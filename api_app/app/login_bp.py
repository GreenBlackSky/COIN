"""
Flask blueprint, that handles user operations.

This module contains methods to create new user or
to get access to existing one.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, \
    current_user

from common.debug_tools import log_request, log_function
from common.schemas import UserSchema
# from common.constants import ENTITY

from .api_app_common import parse_request
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
@log_request
@jwt_required(optional=True)
def create_user():
    """
    Register new user.

    Global variable `request` must contain
     `name` and `password` fields.
    """
    if current_user:
        return {'status': 'already authorized'}

    try:
        password, name = parse_request(request, ('password', 'name'))
    except Exception as e:
        return {'status': str(e)}

    result = rpc.core_service.create_user(name, password)
    if result['status'] == 'OK':
        result['access_token'] = create_access_token(identity=result['user'])
    return result


@bp.route("/login", methods=["POST"])
@log_request
def login():
    """
    Log in user.

    Global variable `request` must contain `name` and `password` fields.
    """
    try:
        name, password = parse_request(request, ('name', 'password'))
    except Exception as e:
        return {'status': str(e)}

    result = rpc.core_service.get_user(name, password)
    if result['status'] == 'OK':
        result['access_token'] = create_access_token(identity=result['user'])
    elif result['status'] == 'wrong password':
        return result, 405
    return result


@bp.route("/edit_user", methods=['POST'])
@jwt_required()
@log_request
def edit_user():
    """Edit user."""
    try:
        name, old_pass, new_pass = parse_request(
            request,
            ('name',),
            ('old_pass', 'new_pass')
        )
    except Exception as e:
        return {'status': str(e)}

    result = rpc.core_service.edit_user(
        UserSchema().dump(current_user), name,
        old_pass, new_pass
    )
    if result['status'] == 'wrong password':
        return result, 405
    return result


@bp.route("/logout", methods=['POST'])
@log_request
@jwt_required()
def logout():
    """Log out user."""
    return {"status": "OK"}
