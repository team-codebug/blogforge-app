from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from . import bp
from ..extensions import db
from ..models import Post


@bp.get('/')
@login_required
def list_posts():
	posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.updated_at.desc()).all()
	return render_template('posts/list.html', posts=posts)


@bp.get('/new')
@login_required
def new_post():
	return render_template('posts/edit.html', post=None)


@bp.post('/')
@login_required
def create_post():
	title = request.form.get('title', '').strip()
	content = request.form.get('content', '').strip()
	if not title:
		return redirect(url_for('posts.new_post'))
	post = Post(user_id=current_user.id, title=title, slug=title.lower().replace(' ', '-'), content_markdown=content)
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
	return render_template('posts/edit.html', post=post)


@bp.post('/<int:post_id>')
@login_required
def update_post(post_id: int):
	post = Post.query.filter_by(id=post_id, user_id=current_user.id).first()
	if not post:
		abort(404)
	post.title = request.form.get('title', post.title)
	post.content_markdown = request.form.get('content', post.content_markdown)
	db.session.commit()
	return redirect(url_for('posts.edit_post', post_id=post.id))
