"""Flask blueprint, that handles user operations."""

from hashlib import md5

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, \
    get_current_user

from common.debug_tools import log_request, log_function
from common.schemas import UserSchema
# from common.constants import ENTITY

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
     `email` and `password` fields.
    """
    if get_current_user():
        return {'status': 'already authorized'}

    try:
        password, email = parse_request(request, ('password', 'email'))
    except Exception as e:
        return {'status': str(e)}

    password_hash = md5(password.encode()).hexdigest()
    user = rpc.db_service.create_user(email, password_hash)
    if user is None:
        return {'status': 'user already exists'}
    user = UserSchema().load(user)

    return jsonify({
        'status': 'OK',
        'access_token': create_access_token(identity=user),
        'user': UserSchema().dump(user)
    })


@bp.route("/login", methods=["POST"])
@log_request
def login():
    """
    Log in user.

    Global variable `request` must contain `email` and `password` fields.
    """
    try:
        email, password = parse_request(request, ('email', 'password'))
    except Exception as e:
        return {'status': str(e)}

    user = rpc.db_service.get_user(email=email)
    if user is None:
        return {'status': 'no such user'}
    user = UserSchema().load(user)
    if user.pass_hash != md5(password.encode()).hexdigest():
        return {'status': 'wrong password'}

    return {
        'status': 'OK',
        'access_token': create_access_token(identity=user),
        'user': UserSchema().dump(user)
    }


@bp.route("/edit_user", methods=['POST'])
@log_request
@jwt_required()
def edit_user():
    """Edit user."""
    try:
        email, old_pass, new_pass = parse_request(
            request,
            ('email',),
            ('old_pass', 'new_pass')
        )
    except Exception as e:
        return {'status': str(e)}

    got_old_pass = (old_pass is not None)
    got_new_pass = (new_pass is not None)
    if got_new_pass != got_old_pass:
        return {'status': "new password must be provided with an old password"}

    user = get_current_user()
    if got_old_pass and got_new_pass:
        old_hash = md5(old_pass.encode()).hexdigest()
        if old_hash != user.pass_hash:
            return {'status': 'wrong password'}, 405
        new_hash = md5(new_pass.encode()).hexdigest()
    else:
        new_hash = None

    if email != user.email:
        other_user = rpc.db_service.get_user(email=email)
        if other_user:
            return {'status': 'user already exists'}

    return {
        'status': 'OK',
        'user': rpc.db_service.update_user(user.id, email, new_hash)
    }


@bp.route("/logout", methods=['POST'])
@log_request
@jwt_required()
def logout():
    """Log out user."""
    return {"status": "OK"}
