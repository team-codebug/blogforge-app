from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from . import bp
from ..extensions import login_manager
from ..models import User, Post


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
	# Get all published posts from all users, sorted by latest first
	published_posts = Post.query.filter_by(is_published=True).order_by(Post.updated_at.desc()).all()
	
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
	
	return render_template('main/dashboard.html', posts=published_posts, tag_colors=tag_colors)


@bp.get('/profile')
@login_required
def profile():
	# Calculate statistics
	total_posts = len(current_user.posts)
	published_posts = len([post for post in current_user.posts if post.is_published])
	draft_posts = total_posts - published_posts
	
	# Get unique tags count
	all_tags = set()
	for post in current_user.posts:
		all_tags.update(post.tags)
	unique_tags_count = len(all_tags)
	
	stats = {
		'total_posts': total_posts,
		'published_posts': published_posts,
		'draft_posts': draft_posts,
		'unique_tags_count': unique_tags_count
	}
	
	return render_template('main/profile.html', user=current_user, stats=stats)


@bp.get('/api/blog/<int:post_id>')
@login_required
def get_blog_content(post_id):
	"""Get blog content for overlay display"""
	post = Post.query.filter_by(id=post_id, is_published=True).first()
	if not post:
		return jsonify({'error': 'Blog not found'}), 404
	
	# Get author information
	author = post.user
	
	return jsonify({
		'id': post.id,
		'title': post.title,
		'description': post.description,
		'content': post.content_markdown,
		'author': {
			'name': author.name,
			'avatar_url': author.avatar_url
		},
		'created_at': post.created_at.isoformat(),
		'updated_at': post.updated_at.isoformat(),
		'tags': [{'name': tag.name} for tag in post.tags]
	})
