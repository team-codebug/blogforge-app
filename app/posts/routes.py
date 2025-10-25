from flask import render_template, request, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from . import bp
from ..extensions import db
from ..models import Blog, Tag
from markdown_it import MarkdownIt
from datetime import datetime


@bp.get('/')
@login_required
def list_blogs():
	# Get filter parameter from query string
	filter_type = request.args.get('filter', 'published')
	
	# Base query for user's blogs
	query = Blog.query.filter_by(user_id=current_user.id)
	
	# Apply filter based on parameter
	if filter_type == 'drafts':
		blogs = query.filter_by(is_published=False).order_by(Blog.updated_at.desc()).all()
	elif filter_type == 'published':
		blogs = query.filter_by(is_published=True).order_by(Blog.updated_at.desc()).all()
	else:
		# Default to all blogs if no valid filter
		blogs = query.order_by(Blog.updated_at.desc()).all()
	
	# Define tag colors for random assignment - dark backgrounds with white text
	tag_colors = [
		'bg-blue-600 text-white',
		'bg-green-600 text-white',
		'bg-purple-600 text-white',
		'bg-pink-600 text-white',
		'bg-yellow-600 text-white',
		'bg-indigo-600 text-white',
		'bg-red-600 text-white',
		'bg-orange-600 text-white',
		'bg-teal-600 text-white',
		'bg-cyan-600 text-white'
	]
	
	return render_template('posts/list.html', blogs=blogs, tag_colors=tag_colors, current_filter=filter_type)


@bp.get('/new')
@login_required
def new_blog():
	return render_template('posts/edit.html', blog=None, available_tags=[], current_tag_ids=[])


@bp.post('/')
@login_required
def create_blog():
	title = request.form.get('title', '').strip()
	description = request.form.get('description', '').strip()
	content = request.form.get('content', '').strip()
	if not title:
		return redirect(url_for('posts.new_blog'))
	
	# Create blog as published by default
	blog = Blog(
		user_id=current_user.id, 
		title=title, 
		slug=title.lower().replace(' ', '-'), 
		description=description, 
		content_markdown=content,
		is_published=True,  # Set as published by default
		published_at=datetime.utcnow()  # Set publish timestamp
	)
	db.session.add(blog)
	db.session.commit()
	return redirect(url_for('posts.edit_blog', blog_id=blog.id))


@bp.get('/<int:blog_id>')
@login_required
def view_blog(blog_id: int):
	blog = Blog.query.filter_by(id=blog_id, user_id=current_user.id).first()
	if not blog:
		abort(404)
	return render_template('posts/detail.html', blog=blog)


@bp.get('/<int:blog_id>/edit')
@login_required
def edit_blog(blog_id: int):
	blog = Blog.query.filter_by(id=blog_id, user_id=current_user.id).first()
	if not blog:
		abort(404)
	
	# Get all user's tags and current blog tags
	available_tags = Tag.query.filter_by(user_id=current_user.id).order_by(Tag.name).all()
	current_tag_ids = [tag.id for tag in blog.tags]
	
	return render_template('posts/edit.html', blog=blog, available_tags=available_tags, current_tag_ids=current_tag_ids)


@bp.post('/<int:blog_id>')
@login_required
def update_blog(blog_id: int):
	blog = Blog.query.filter_by(id=blog_id, user_id=current_user.id).first()
	if not blog:
		abort(404)
	
	# Update basic fields
	blog.title = request.form.get('title', blog.title)
	blog.description = request.form.get('description', blog.description)
	blog.content_markdown = request.form.get('content', blog.content_markdown)
	
	# Preserve existing AI-generated content (don't overwrite if not provided in form)
	# LinkedIn and Twitter content are only updated via AI endpoints, not regular saves
	
	# Ensure blog is published when saving
	blog.is_published = True
	if not blog.published_at:  # Set publish timestamp if not already set
		blog.published_at = datetime.utcnow()
	
	# Handle tag assignments
	selected_tag_ids = request.form.getlist('tags')
	selected_tag_ids = [int(tag_id) for tag_id in selected_tag_ids if tag_id.isdigit()]
	
	# Get tags that belong to the current user
	user_tags = Tag.query.filter_by(user_id=current_user.id).filter(Tag.id.in_(selected_tag_ids)).all()
	
	# Update blog tags
	blog.tags = user_tags
	
	db.session.commit()
	return redirect(url_for('posts.edit_blog', blog_id=blog.id))


@bp.get('/tags')
@login_required
def list_tags():
	tags = Tag.query.filter_by(user_id=current_user.id).order_by(Tag.name).all()
	return render_template('posts/tags.html', tags=tags)


@bp.post('/tags')
@login_required
def create_tag():
	name = request.form.get('name', '').strip().lower()
	if not name:
		return redirect(url_for('posts.list_tags'))
	
	# Check if tag already exists
	existing_tag = Tag.query.filter_by(user_id=current_user.id, name=name).first()
	if existing_tag:
		return redirect(url_for('posts.list_tags'))
	
	tag = Tag(user_id=current_user.id, name=name)
	db.session.add(tag)
	db.session.commit()
	return redirect(url_for('posts.list_tags'))


@bp.delete('/tags/<int:tag_id>')
@login_required
def delete_tag(tag_id: int):
	tag = Tag.query.filter_by(id=tag_id, user_id=current_user.id).first()
	if not tag:
		abort(404)
	db.session.delete(tag)
	db.session.commit()
	return '', 204


@bp.route('/render-markdown', methods=['GET'])
def render_markdown():
	"""Render markdown to HTML using markdown-it-py with proper configuration"""
	markdown_text = request.args.get('text', '')
	if not markdown_text:
		return jsonify({'html': ''})
	
	# Configure markdown-it with proper settings like in the image
	md = MarkdownIt('commonmark', {'breaks': True, 'html': True})
	
	# Enable plugins for enhanced features
	md.enable(['table', 'strikethrough'])
	
	html = md.render(markdown_text)
	print(f"Rendering markdown: '{markdown_text}' -> '{html}'")
	return jsonify({'html': html})


@bp.route('/auto-save', methods=['POST'])
@login_required
def auto_save():
	"""Auto-save post content without updating timestamps"""
	try:
		data = request.get_json()
		blog_id = data.get('blog_id')
		title = data.get('title', '').strip()
		description = data.get('description', '').strip()
		content = data.get('content', '').strip()
		
		if not blog_id:
			return jsonify({'error': 'Blog ID required'}), 400
		
		# Get the blog and verify ownership
		blog = Blog.query.filter_by(id=blog_id, user_id=current_user.id).first()
		if not blog:
			return jsonify({'error': 'Blog not found'}), 404
		
		# Update content without changing updated_at timestamp
		blog.title = title
		blog.description = description
		blog.content_markdown = content
		
		# Ensure blog is published when auto-saving
		blog.is_published = True
		if not blog.published_at:  # Set publish timestamp if not already set
			blog.published_at = datetime.utcnow()
		
		# Don't update updated_at for auto-save
		db.session.commit()
		
		return jsonify({'success': True, 'message': 'Auto-saved successfully'})
		
	except Exception as e:
		print(f"Auto-save error: {e}")
		return jsonify({'error': 'Auto-save failed'}), 500


@bp.route('/save-draft', methods=['POST'])
@login_required
def save_draft():
	"""Save post as draft when user cancels"""
	try:
		data = request.get_json()
		title = data.get('title', '').strip()
		description = data.get('description', '').strip()
		content = data.get('content', '').strip()
		
		if not title:
			return jsonify({'error': 'Title required'}), 400
		
		# Create post as draft
		blog = Blog(
			user_id=current_user.id,
			title=title,
			slug=title.lower().replace(' ', '-'),
			description=description,
			content_markdown=content,
			is_published=False,  # Save as draft
			published_at=None
		)
		db.session.add(blog)
		db.session.commit()
		
		return jsonify({'success': True, 'message': 'Saved as draft', 'blog_id': blog.id})
		
	except Exception as e:
		print(f"Save draft error: {e}")
		return jsonify({'error': 'Failed to save draft'}), 500
