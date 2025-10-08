from datetime import datetime
from sqlalchemy import Enum
from .extensions import db


post_tags = db.Table(
	'post_tags',
	db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
	db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
)


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True, index=True, nullable=False)
	name = db.Column(db.String(255), nullable=True)
	avatar_url = db.Column(db.String(512), nullable=True)
	google_sub = db.Column(db.String(255), unique=True, index=True, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

	posts = db.relationship('Post', backref='user', lazy=True)
	social_posts = db.relationship('SocialPost', backref='user', lazy=True)


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
	title = db.Column(db.String(255), nullable=False)
	slug = db.Column(db.String(255), index=True, nullable=False)
	content_markdown = db.Column(db.Text, nullable=False)
	content_html = db.Column(db.Text, nullable=True)
	summary = db.Column(db.Text, nullable=True)
	is_published = db.Column(db.Boolean, default=False, nullable=False)
	published_at = db.Column(db.DateTime, nullable=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
	updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

	tags = db.relationship('Tag', secondary=post_tags, lazy='subquery', backref=db.backref('posts', lazy=True))


class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
	name = db.Column(db.String(64), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class SocialPost(db.Model):
	__tablename__ = 'social_posts'
	id = db.Column(db.Integer, primary_key=True)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), index=True, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True, nullable=False)
	platform = db.Column(Enum('linkedin', 'twitter', name='social_platform'), nullable=False)
	payload_json = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

	post = db.relationship('Post', backref='social_posts')
