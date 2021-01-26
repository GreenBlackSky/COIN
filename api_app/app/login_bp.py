"""Flask blueprint, that handles user operations."""

import logging
from hashlib import md5
from functools import wraps

from flask import Blueprint, request
from flask_login import login_user, login_required, current_user, logout_user

from . import rpc, login_manager
from .schemas import UserSchema


# TODO refactor
bp = Blueprint('login_bp', __name__)


def log_method(method):
    """Decorate method for logging its input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        logging.debug(f"start {method.__name__}")
        ret = method(*args, **kargs)
        logging.debug(f"finish {method.__name__}")
        return ret
    return _wrapper


@bp.route("/register", methods=['POST'])
@log_method
def register():
    """Register new user."""
    name = request.args.get('name')
    password = request.args.get('password')
    if name is None or password is None:
        return {'status': 'incomplete user data'}
    password_hash = md5(password.encode()).hexdigest()  # TODO use actual hashing
    user = rpc.db_service.create_user(name, password_hash)
    if user is None:
        return {'status': 'service problem'}
    user = UserSchema().load(user)
    login_user(user)
    return {'status': 'OK'}


@bp.route("/login", methods=['POST'])
@log_method
def login():
    """Log in user."""
    name = request.args.get('name')
    password = request.args.get('password')
    if name is None or password is None:
        return {'status': 'incomplete user data'}
    password_hash = md5(password.encode()).hexdigest()
    user = rpc.cache_service.get_user_by_name(name)
    if user is None:
        return {'status': 'service problem'}
    user = UserSchema().load(user)
    if user.password_hash != password_hash:
        return {'status': 'WRONG PASSWORD'}
    login_user(user)
    return {'status': 'OK'}


@login_required
@bp.route("/logout", methods=['POST'])
@log_method
def logout():
    """Log out user."""
    logout_user()
    return {"status": "OK"}


@login_manager.user_loader
@log_method
def load_user(user_id):
    """Load user handler."""
    user = rpc.cache_service.get_user(user_id)
    if user is None:
        return None
    return UserSchema().load(user)


@login_manager.unauthorized_handler
@log_method
def unauthorized():
    """Unauthorized access handler."""
    return {"status": "Unauthorized access"}
