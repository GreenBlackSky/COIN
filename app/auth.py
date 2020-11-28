"""Authentification stuff."""

from datetime import datetime
from flask import Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from .models import db, User
from . import login_manager


bp = Blueprint('auth_bp', __name__, template_folder='templates')


@bp.route("/signup", methods=('POST',))
def signup():
    """Register new user."""
    name = request.args.get('name')
    password = request.args.get
    if name is None or password is None:
        return

    existing_user = User.query.filter_by(name=name).first()
    if existing_user is not None:
        return

    user = User(
        name=name,
        created_on=datetime.now(),
        last_login=datetime.now()
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return {"signed up": name}


@bp.route("/login", methods=('POST',))
def login():
    """Log in user."""
    if current_user.is_authenticated:
        return

    name = request.args.get('name')
    password = request.args.get
    if name is None or password is None:
        return

    user = User.query.filter_by(name=name).first()
    if user is None or not user.check_password(password=password):
        return

    login_user(user)
    user.last_login = datetime.now()
    db.session.add(user)
    db.session.commit()
    return {"logged in": name}


@bp.route("/logout", methods=('POST',))
@login_required
def logout():
    """Log out user."""
    logout_user()


@login_manager.user_loader
def load_user(user_id):
    """Get current user (tech)."""
    if user_id is not None:
        return User.query.get(user_id)
    return


@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access."""
    return {"unathorized user": ""}
