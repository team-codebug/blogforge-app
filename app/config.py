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
	OAUTH_GOOGLE_CLIENT_ID = os.getenv('OAUTH_GOOGLE_CLIENT_ID')
	OAUTH_GOOGLE_CLIENT_SECRET = os.getenv('OAUTH_GOOGLE_CLIENT_SECRET')
	OAUTH_GOOGLE_REDIRECT_URI = os.getenv('OAUTH_GOOGLE_REDIRECT_URI', 'http://127.0.0.1:5000/auth/google/callback')

	# AI Providers
	AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')  # or 'gemini'
	OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'AIzaSyAgC9qfvudROdDHwy6XQdSatSDK_Hdkqro')
	GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


class DevelopmentConfig(BaseConfig):
	DEBUG = True


class TestingConfig(BaseConfig):
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
	SECRET_KEY = 'test-secret-key'


class ProductionConfig(BaseConfig):
	SESSION_COOKIE_SECURE = True


def get_config(config_name: str | None):
	if config_name is None:
		config_name = os.getenv('FLASK_ENV', 'development')
	mapping = {
		'development': DevelopmentConfig,
		'testing': TestingConfig,
		'production': ProductionConfig,
	}
	return mapping.get(config_name, DevelopmentConfig)