"""
Flask blueprint, that handles user operations.

This module contains methods to create new user or
to get access to existing one.
"""

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, \
    current_user

from common.debug_tools import wrap_request, log_function
from common.schemas import UserSchema

from . import rpc, jwt


bp = Blueprint('login_bp', __name__)


@jwt.user_identity_loader
@log_function
def _user_identity_lookup(user_json):
    return user_json['id']


@jwt.user_lookup_loader
@log_function
def _user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = rpc.db_service.get_user(user_id=identity)
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
@jwt_required(optional=True)
@wrap_request('name', 'password')
def create_user(name, password):
    """
    Register new user.

    Global variable `request` must contain
     `name` and `password` fields.
    """
    if current_user:
        return {'status': 'already authorized'}

    result = rpc.core_service.create_user(name, password)
    if result['status'] == 'OK':
        result['access_token'] = create_access_token(identity=result['user'])
    return result


@bp.route("/login", methods=["POST"])
@wrap_request('name', 'password')
def login(name, password):
    """
    Log in user.

    Global variable `request` must contain `name` and `password` fields.
    """
    result = rpc.core_service.validate_user(name, password)
    if result['status'] == 'OK':
        result['access_token'] = create_access_token(identity=result['user'])
    elif result['status'] == 'wrong password':
        return result, 405
    return result


@bp.route("/edit_user", methods=['POST'])
@jwt_required()
@wrap_request('name', optional_arg_names=('old_pass', 'new_pass'))
def edit_user(name, old_pass=None, new_pass=None):
    """Edit user."""
    result = rpc.core_service.edit_user(
        UserSchema().dump(current_user), name,
        old_pass, new_pass
    )
    if result['status'] == 'wrong password':
        return result, 405
    return result


@bp.route("/logout", methods=['POST'])
@wrap_request()
@jwt_required()
def logout():
    """Log out user."""
    return {"status": "OK"}
