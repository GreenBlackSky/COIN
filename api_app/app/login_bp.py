"""Flask blueprint, that handles user operations."""

from hashlib import md5

from flask import Blueprint, request
from flask_login import login_user, login_required, current_user, logout_user

from common.debug_tools import log_request
from common.schemas import UserSchema

from . import rpc, login_manager


bp = Blueprint('login_bp', __name__)


@bp.route("/register", methods=['POST'])
@log_request
def register():
    """
    Register new user.

    Global variable `request` must contain `name` and `password` fields.
    """
    if current_user.is_authenticated:
        return {'status': 'already authorized'}
    name = request.args.get('name')
    password = request.args.get('password')
    if name is None or password is None:
        return {'status': 'incomplete user data'}
    password_hash = md5(password.encode()).hexdigest()  # TODO use actual hashing
    user = rpc.db_service.create_user(name, password_hash)
    if user is None:
        return {'status': 'user already exists'}
    user = UserSchema().load(user)
    login_user(user)
    return {'status': 'OK'}


@bp.route("/login", methods=['POST'])
@log_request
def login():
    """
    Log in user.

    Global variable `request` must contain `name` and `password` fields.
    """
    name = request.args.get('name')
    password = request.args.get('password')
    if name is None or password is None:
        return {'status': 'incomplete user data'}
    password_hash = md5(password.encode()).hexdigest()
    user = rpc.db_service.get_user_by_name(name)
    if user is None:
        return {'status': 'no such user'}
    user = UserSchema().load(user)
    if user.password_hash != password_hash:
        return {'status': 'wrong password'}
    login_user(user)
    return {'status': 'OK'}


@login_required
@bp.route("/logout", methods=['POST'])
@log_request
def logout():
    """Log out user."""
    logout_user()
    return {"status": "OK"}


@login_manager.user_loader
@log_request
def load_user(user_id):
    """Load user handler."""
    user = rpc.cache_service.get_user(user_id)
    if user is None:
        return None
    return UserSchema().load(user)


@login_manager.unauthorized_handler
@log_request
def unauthorized():
    """Unauthorized access handler."""
    return {"status": "unauthorized access"}
