from flask import render_template, request, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from . import bp
from ..extensions import db
from ..models import Post, Tag
from markdown_it import MarkdownIt
from datetime import datetime


@bp.get('/')
@login_required
def list_posts():
	# Get filter parameter from query string
	filter_type = request.args.get('filter', 'published')
	
	# Base query for user's posts
	query = Post.query.filter_by(user_id=current_user.id)
	
	# Apply filter based on parameter
	if filter_type == 'drafts':
		posts = query.filter_by(is_published=False).order_by(Post.updated_at.desc()).all()
	elif filter_type == 'published':
		posts = query.filter_by(is_published=True).order_by(Post.updated_at.desc()).all()
	else:
		# Default to all posts if no valid filter
		posts = query.order_by(Post.updated_at.desc()).all()
	
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
	
	return render_template('posts/list.html', posts=posts, tag_colors=tag_colors, current_filter=filter_type)


@bp.get('/new')
@login_required
def new_post():
	return render_template('posts/edit.html', post=None, available_tags=[], current_tag_ids=[])


@bp.post('/')
@login_required
def create_post():
	title = request.form.get('title', '').strip()
	description = request.form.get('description', '').strip()
	content = request.form.get('content', '').strip()
	if not title:
		return redirect(url_for('posts.new_post'))
	
	# Create post as published by default
	post = Post(
		user_id=current_user.id, 
		title=title, 
		slug=title.lower().replace(' ', '-'), 
		description=description, 
		content_markdown=content,
		is_published=True,  # Set as published by default
		published_at=datetime.utcnow()  # Set publish timestamp
	)
	db.session.add(post)
	db.session.commit()
	return redirect(url_for('posts.edit_post', post_id=post.id))


@bp.get('/<int:post_id>')
@login_required
def view_post(post_id: int):
	post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()
	if not post:
		abort(404)
	return render_template('posts/detail.html', post=post)


@bp.get('/<int:post_id>/edit')
@login_required
def edit_post(post_id: int):
	post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()
	if not post:
		abort(404)
	
	# Get all user's tags and current post tags
	available_tags = Tag.query.filter_by(user_id=current_user.id).order_by(Tag.name).all()
	current_tag_ids = [tag.id for tag in post.tags]
	
	return render_template('posts/edit.html', post=post, available_tags=available_tags, current_tag_ids=current_tag_ids)


@bp.post('/<int:post_id>')
@login_required
def update_post(post_id: int):
	post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()
	if not post:
		abort(404)
	
	# Update basic fields
	post.title = request.form.get('title', post.title)
	post.description = request.form.get('description', post.description)
	post.content_markdown = request.form.get('content', post.content_markdown)
	
	# Ensure post is published when saving
	post.is_published = True
	if not post.published_at:  # Set publish timestamp if not already set
		post.published_at = datetime.utcnow()
	
	# Handle tag assignments
	selected_tag_ids = request.form.getlist('tags')
	selected_tag_ids = [int(tag_id) for tag_id in selected_tag_ids if tag_id.isdigit()]
	
	# Get tags that belong to the current user
	user_tags = Tag.query.filter_by(user_id=current_user.id).filter(Tag.id.in_(selected_tag_ids)).all()
	
	# Update post tags
	post.tags = user_tags
	
	db.session.commit()
	return redirect(url_for('posts.edit_post', post_id=post.id))


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
		post_id = data.get('post_id')
		title = data.get('title', '').strip()
		description = data.get('description', '').strip()
		content = data.get('content', '').strip()
		
		if not post_id:
			return jsonify({'error': 'Post ID required'}), 400
		
		# Get the post and verify ownership
		post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()
		if not post:
			return jsonify({'error': 'Post not found'}), 404
		
		# Update content without changing updated_at timestamp
		post.title = title
		post.description = description
		post.content_markdown = content
		
		# Ensure post is published when auto-saving
		post.is_published = True
		if not post.published_at:  # Set publish timestamp if not already set
			post.published_at = datetime.utcnow()
		
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
		post = Post(
			user_id=current_user.id,
			title=title,
			slug=title.lower().replace(' ', '-'),
			description=description,
			content_markdown=content,
			is_published=False,  # Save as draft
			published_at=None
		)
		db.session.add(post)
		db.session.commit()
		
		return jsonify({'success': True, 'message': 'Saved as draft', 'post_id': post.id})
		
	except Exception as e:
		print(f"Save draft error: {e}")
		return jsonify({'error': 'Failed to save draft'}), 500
