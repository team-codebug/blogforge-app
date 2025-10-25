from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from . import bp
from ..extensions import login_manager
from ..models import User, Blog


@login_manager.user_loader
def load_user(user_id: str):
	return User.query.get(int(user_id))


@bp.get('/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('main.dashboard'))
	return render_template('main/index.html')


@bp.get('/dashboard')
@login_required
def dashboard():
	# Get search query from URL parameters
	search_query = request.args.get('q', '').strip()
	
	# Start with base query for published blogs
	query = Blog.query.filter_by(is_published=True)
	
	# Apply search filter if query is provided
	if search_query:
		# Search in title, description, and tags
		from sqlalchemy import or_
		from ..models import Tag
		
		# Create search conditions
		search_conditions = [
			Blog.title.ilike(f'%{search_query}%'),
			Blog.description.ilike(f'%{search_query}%')
		]
		
		# Add tag search condition
		search_conditions.append(
			Blog.tags.any(Tag.name.ilike(f'%{search_query}%'))
		)
		
		# Apply the search conditions
		query = query.filter(or_(*search_conditions))
	
	# Get blogs sorted by latest first
	published_blogs = query.order_by(Blog.updated_at.desc()).all()
	
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
	
	return render_template('main/dashboard.html', blogs=published_blogs, tag_colors=tag_colors, search_query=search_query)


@bp.get('/profile')
@login_required
def profile():
	# Calculate statistics
	total_blogs = len(current_user.blogs)
	published_blogs = len([blog for blog in current_user.blogs if blog.is_published])
	draft_blogs = total_blogs - published_blogs
	
	# Get unique tags count
	all_tags = set()
	for blog in current_user.blogs:
		all_tags.update(blog.tags)
	unique_tags_count = len(all_tags)
	
	stats = {
		'total_blogs': total_blogs,
		'published_blogs': published_blogs,
		'draft_blogs': draft_blogs,
		'unique_tags_count': unique_tags_count
	}
	
	return render_template('main/profile.html', user=current_user, stats=stats)


@bp.get('/api/blog/<int:blog_id>')
@login_required
def get_blog_content(blog_id):
	"""Get blog content for overlay display"""
	blog = Blog.query.filter_by(id=blog_id, is_published=True).first()
	if not blog:
		return jsonify({'error': 'Blog not found'}), 404
	
	# Get author information
	author = blog.user
	
	return jsonify({
		'id': blog.id,
		'title': blog.title,
		'description': blog.description,
		'content': blog.content_markdown,
		'author': {
			'name': author.name,
			'avatar_url': author.avatar_url
		},
		'created_at': blog.created_at.isoformat(),
		'updated_at': blog.updated_at.isoformat(),
		'tags': [{'name': tag.name} for tag in blog.tags]
	})
