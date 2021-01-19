"""Flask blueprint, that handles user operations."""

from hashlib import md5

from flask import Blueprint, request
from flask_login import login_user, login_required, current_user, logout_user

from . import rpc, LoginManager

bp = Blueprint('login_bp', __name__)

# TODO refactor


@bp.route("/register", methods=['POST'])
def register():
    """Register new user."""
    name = request.args.get('name')
    password = request.args.get('password')
    if name is None or password is None:
        return {'status': 'incomplete user data'}
    password_hash = md5(password).hexdigest()  # TODO use actual hashing
    user = rpc.db_service.create_user(name, password_hash)
    if user is None:
        return {'status': 'service problem'}
    login_user(user)
    return {'status': 'OK'}


@bp.route("/login", methods=['POST'])
def login():
    """Log in user."""
    name = request.args.get('name')
    password = request.args.get('password')
    if name is None or password is None:
        return {'status': 'incomplete user data'}
    password_hash = md5(password).hexdigest()
    user = rpc.cache_service.get_user_by_name(name)
    if user is None:
        return {'status': 'service problem'}
    if user.password_hash != password_hash:
        return {'status': 'WRONG PASSWORD'}
    login_user(user)
    return {'status': 'OK'}


@login_required
@bp.route("/logout", methods=['POST'])
def logout():
    """Log out user."""
    logout_user()
    return {"status": "OK"}


@login_manager.user_loader
def load_user(user_id):
    """Load user handler."""
    user = rpc.cache_service.get_user(user_id)  # use marshmallow
    return user


@login_manager.unauthorized_handler
def unauthorized():
    """Unauthorized access handler."""
    return {"user_id": None}
