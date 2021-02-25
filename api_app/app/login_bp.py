"""Flask blueprint, that handles user operations."""

from hashlib import md5

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_current_user

from common.debug_tools import log_request, log_function
from common.schemas import UserSchema

from . import rpc, jwt


bp = Blueprint('login_bp', __name__)


@jwt.user_identity_loader
@log_function
def _user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
@log_function
def _user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = rpc.cache_service.get_user(identity)
    if user is None:
        return None
    return UserSchema().load(user)


@jwt.unauthorized_loader
@log_function
def unauthorized(reason):
    """Handle unauthirized access."""
    return {
        "status": "unauthorized access",
        "reason": reason
        }, 401


@bp.route("/register", methods=['POST'])
@log_request
@jwt_required(optional=True)
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
@log_request
@jwt_required(optional=True)
def login():
    """
    Log in user.

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
    password_hash = md5(password.encode()).hexdigest()
    result = rpc.db_service.check_user(name, password_hash)
    if result and result.get('status') == 'OK':
        user = UserSchema().load(
            rpc.cache_service.get_user(result['user_id'])
        )
    else:
        return result
    access_token = create_access_token(identity=user)
    return {
        'status': 'OK',
        'access_token': access_token
    }


@bp.route("/logout", methods=['POST'])
@log_request
@jwt_required()
def logout():
    """Log out user."""
    # TODO balcklist token
    rpc.cache_service.forget_user(get_current_user().id)
    return {"status": "OK"}
