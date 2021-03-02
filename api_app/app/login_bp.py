"""Flask blueprint, that handles user operations."""

from hashlib import md5

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, \
    get_current_user

from common.debug_tools import log_request, log_function
from common.schemas import UserSchema
from .api_app_common import parse_request
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
def create_user():
    """
    Register new user.

    Global variable `request` must contain `name`,
     `email` and `password` fields.
    """
    if get_current_user():
        return {'status': 'already authorized'}

    try:
        name, password, email = parse_request(
            request,
            ('name', 'password', 'email')
        )
    except Exception as e:
        return {'status': str(e)}

    password_hash = md5(password.encode()).hexdigest()
    user = rpc.db_service.create_user(name, email, password_hash)
    if user is None:
        return {'status': 'user already exists'}
    user = UserSchema().load(user)

    return jsonify({
        'status': 'OK',
        'access_token': create_access_token(identity=user)
    })


@bp.route("/login", methods=["POST"])
@log_request
@jwt_required(optional=True)
def login():
    """
    Log in user.

    Global variable `request` must contain `email` and `password` fields.
    """
    if get_current_user():
        return {'status': 'already authorized'}

    try:
        email, password = parse_request(request, ('email', 'password'))
    except Exception as e:
        return {'status': str(e)}

    password_hash = md5(password.encode()).hexdigest()

    result = rpc.db_service.check_user(email, password_hash)
    if result and result.get('status') == 'OK':
        user = UserSchema().load(
            rpc.cache_service.get_user(result['user_id'])
        )
    else:
        return result

    return {
        'status': 'OK',
        'access_token': create_access_token(identity=user),
        'name': user.name
    }


@bp.route("/logout", methods=['POST'])
@log_request
@jwt_required()
def logout():
    """Log out user."""
    # TODO balcklist token
    rpc.cache_service.forget_user(get_current_user().id)
    return {"status": "OK"}
