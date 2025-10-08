from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf_protect = CSRFProtect()

oauth = OAuth()


def _rate_limit_key_func():
	try:
		# Defer import to avoid circulars
		from flask_login import current_user
		if getattr(current_user, 'is_authenticated', False):
			return f"user:{getattr(current_user, 'id', 'anon')}"
	except Exception:
		pass
	return get_remote_address()


limiter = Limiter(key_func=_rate_limit_key_func, default_limits=[])
