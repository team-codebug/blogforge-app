from flask import Flask
from .config import get_config
from .extensions import (
	db,
	migrate,
	login_manager,
	csrf_protect,
	limiter,
	oauth,
)


def create_app(config_name: str | None = None) -> Flask:
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(get_config(config_name))

	# Ensure instance folder exists
	try:
		import os
		os.makedirs(app.instance_path, exist_ok=True)
	except OSError:
		pass

	# init extensions
	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	login_manager.login_view = 'auth.login'
	csrf_protect.init_app(app)
	limiter.init_app(app)
	oauth.init_app(app)
	
	# Exempt markdown rendering endpoint from CSRF protection
	csrf_protect.exempt('posts.render_markdown')

	# register blueprints
	from .auth import bp as auth_bp
	from .posts import bp as posts_bp
	from .ai import bp as ai_bp
	from .main import bp as main_bp

	app.register_blueprint(auth_bp, url_prefix='/auth')
	app.register_blueprint(posts_bp, url_prefix='/posts')
	app.register_blueprint(ai_bp, url_prefix='/api/ai')
	app.register_blueprint(main_bp)

	return app
