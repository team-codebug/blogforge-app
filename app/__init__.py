from flask import Flask
import json
import os
from dotenv import load_dotenv
from .config import get_config

# Load environment variables from .flaskenv
load_dotenv('.flaskenv')
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
	
	# Set environment variables in Flask config
	app.config['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')

	# Ensure instance folder exists
	try:
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
	
	# Add custom Jinja2 filters
	@app.template_filter('from_json')
	def from_json_filter(value):
		try:
			if not value:
				return []
			# Clean up the value first
			value = str(value).strip()
			# Remove any markdown formatting
			if '```json' in value:
				value = value.split('```json')[1].split('```')[0].strip()
			elif '```' in value:
				value = value.split('```')[1].split('```')[0].strip()
			return json.loads(value)
		except (json.JSONDecodeError, TypeError, AttributeError):
			return []

	return app
