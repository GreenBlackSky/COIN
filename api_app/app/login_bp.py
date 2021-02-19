"""Flask blueprint, that handles user operations."""

from hashlib import md5

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, current_user, jwt_required, get_current_user

from common.debug_tools import log_request, log_method
from common.schemas import UserSchema

from . import rpc, jwt


bp = Blueprint('login_bp', __name__)


@jwt.user_identity_loader
@log_method
def _user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
@log_method
def _user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = rpc.cache_service.get_user(identity)
    if user is None:
        return None
    return UserSchema().load(user)


@jwt.unauthorized_loader
@log_method
def unauthorized(reason):
    """Handle unauthirized access."""
    return {
        "status": "unauthorized access",
        "reason": reason
        }, 401


@bp.route("/register", methods=['POST'])
@jwt_required(optional=True)
@log_request
def register():
    """
    Register new user.

    Global variable `request` must contain `name` and `password` fields.
    """
    if get_current_user():
        return {'status': 'already authorized'}
    request_data = request.get_json()
    if request_data is None:
        return {'status': 'no json data'}
    name = request_data.get('name')
    password = request_data.get('password')
    if name is None or password is None:
        return {'status': 'incomplete user data'}
    password_hash = md5(password.encode()).hexdigest()  # TODO use actual hashing
    user = rpc.db_service.create_user(name, password_hash)
    if user is None:
        return {'status': 'user already exists'}
    user = UserSchema().load(user)
    access_token = create_access_token(identity=user)
    return jsonify({
        'status': 'OK',
        'access_token': access_token
    })


@bp.route("/login", methods=["POST"])
def login():
    """
    Log in user.

    Global variable `request` must contain `name` and `password` fields.
    """
    request_data = request.get_json()
    if request_data is None:
        return {'status': 'no json data'}
    name = request_data.get('name')
    password = request_data.get('password')
    if name is None or password is None:
        return {'status': 'incomplete user data'}
    password_hash = md5(password.encode()).hexdigest()
    user = rpc.db_service.get_user_by_name(name)
    if user is None:
        return {'status': 'no such user'}
    user = UserSchema().load(user)
    if user.password_hash != password_hash:
        return {'status': 'wrong password'}
    access_token = create_access_token(identity=user)
    return {
        'status': 'OK',
        'access_token': access_token
    }


@bp.route("/logout", methods=['POST'])
@jwt_required()
@log_request
def logout():
    """Log out user."""
    # TODO balcklist token
    rpc.cache_service.forget_user(current_user.id)
    return {"status": "OK"}
