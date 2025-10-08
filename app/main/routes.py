from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import bp
from ..extensions import login_manager
from ..models import User


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
	return render_template('main/dashboard.html')
