from flask import redirect, request, url_for, session
from flask import current_app as app
from flask_login import login_user, logout_user
from . import bp
from ..extensions import oauth, db
from ..models import User


@bp.get('/login')
def login():
	google = oauth.register(
		name='google',
		client_id=app.config['OAUTH_GOOGLE_CLIENT_ID'],
		client_secret=app.config['OAUTH_GOOGLE_CLIENT_SECRET'],
		server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
		client_kwargs={'scope': 'openid email profile'},
	)
	redirect_uri = app.config['OAUTH_GOOGLE_REDIRECT_URI']
	return oauth.google.authorize_redirect(redirect_uri)


@bp.get('/callback')
def callback():
	token = oauth.google.authorize_access_token()
	userinfo = token.get('userinfo') or oauth.google.parse_id_token(token)
	if not userinfo:
		return redirect(url_for('main.index'))
	google_sub = userinfo.get('sub')
	email = userinfo.get('email')
	name = userinfo.get('name')
	avatar = userinfo.get('picture')
	user = User.query.filter_by(google_sub=google_sub).first()
	if not user:
		user = User(google_sub=google_sub, email=email, name=name, avatar_url=avatar)
		db.session.add(user)
		db.session.commit()
	login_user(user)
	return redirect(url_for('main.dashboard'))


@bp.post('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.index'))
