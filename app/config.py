import os
from datetime import timedelta


class BaseConfig:
	SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'app.db')))
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	SESSION_COOKIE_HTTPONLY = True
	REMEMBER_COOKIE_DURATION = timedelta(days=14)

	# CSRF
	WTF_CSRF_TIME_LIMIT = None

	# Rate limiting
	RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '1000/day')
	RATELIMIT_STORAGE_URI = os.getenv('RATELIMIT_STORAGE_URI', 'memory://')

	# OAuth
	OAUTH_GOOGLE_CLIENT_ID = os.getenv('OAUTH_GOOGLE_CLIENT_ID', '963038780537-g6ho6e1u4dfsa9avuhds4ha9f6qo5emv.apps.googleusercontent.com')
	OAUTH_GOOGLE_CLIENT_SECRET = os.getenv('OAUTH_GOOGLE_CLIENT_SECRET', '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')
	OAUTH_GOOGLE_REDIRECT_URI = os.getenv('OAUTH_GOOGLE_REDIRECT_URI', 'http://127.0.0.1:5000/auth/google/callback')

	# AI Providers
	AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')  # or 'gemini'
	OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
	GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')


class DevelopmentConfig(BaseConfig):
	DEBUG = True


class ProductionConfig(BaseConfig):
	SESSION_COOKIE_SECURE = True


def get_config(config_name: str | None):
	if config_name is None:
		config_name = os.getenv('FLASK_ENV', 'development')
	mapping = {
		'development': DevelopmentConfig,
		'production': ProductionConfig,
	}
	return mapping.get(config_name, DevelopmentConfig)
