"""
Flask blueprint, that handles user operations.

This module contains methods to create new user or
to get access to existing one.
"""

from datetime import datetime
from hashlib import md5

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, \
    current_user

from common.celery_holder import celery_app
from common.constants import MAIN_ACCOUNT_NAME
from common.debug_tools import log_request, log_function
from common.schemas import UserSchema

from .. import jwt
from ..request_helpers import parse_request_args
from ..model import session, UserModel

from . import account_bp


bp = Blueprint('login_bp', __name__)


@jwt.user_identity_loader
@log_function
def _user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
@log_function
def _user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = session.query(UserModel).get(identity)
    if user is None:
        return None
    return user


@jwt.unauthorized_loader
@log_function
def unauthorized(reason):
    """Handle unauthirized access."""
    return {
        "status": "unauthorized access",
        "reason": reason
    }, 401


@bp.post("/register")
@jwt_required(optional=True)
@parse_request_args(request, ('name', 'password'))
@log_request
def create_user(name, password):
    """
    Register new user.

    Global variable `request` must contain
     `name` and `password` fields.
    """
    if current_user:
        return {'status': 'already authorized'}

    user = session.query(UserModel).filter_by(name=name).first()
    if user:
        return {'status': 'user exists'}

    password_hash = md5(password.encode()).hexdigest()
    user = UserModel(
        name=name,
        password_hash=password_hash
    )
    session.add(user)
    session.commit()
    celery_app.send_task(
        'app.handlers.account.create_account',
        kwargs={'user_id': user.id, 'name': MAIN_ACCOUNT_NAME}
    ).get()
    # self.db_service.create_starting_labels(account.id)
    # self.db_service.create_starting_templates(account.id)
    return {
        'access_token': create_access_token(identity=user),
        'status': 'OK',
        'user': UserSchema().dump(user)
    }


@bp.post("/login")
@parse_request_args(request, ('name', 'password'))
@log_request
def login(name, password):
    """
    Log in user.

    Global variable `request` must contain `name` and `password` fields.
    """
    user = session.query(UserModel).filter_by(name=name).first()
    if user is None:
        return {'status': 'no such user'}, 401

    if user.password_hash != md5(password.encode()).hexdigest():
        return {'status': 'wrong password'}, 401

    return {
        'status': 'OK',
        'user': UserSchema().dump(user),
        'access_token': create_access_token(identity=user)
    }


@bp.post("/edit_user")
@jwt_required()
@parse_request_args(request, ('name',), ('old_pass', 'new_pass'))
@log_request
def edit_user(name, old_pass=None, new_pass=None):
    """Edit user."""
    if name != current_user.name:
        other_user = session.query(UserModel).filter_by(name=name).first()
        if other_user:
            return {'status': 'user exists'}
    current_user.name = name

    got_old_pass = (old_pass is not None)
    got_new_pass = (new_pass is not None)
    if got_new_pass != got_old_pass:
        return {
            'status':
            "new password must be provided with an old password"
        }, 412

    if got_old_pass and got_new_pass:
        old_hash = md5(old_pass.encode()).hexdigest()
        if old_hash != current_user.password_hash:
            return {'status': 'wrong password'}, 401
        new_hash = md5(new_pass.encode()).hexdigest()
        current_user.password_hash = new_hash

    session.commit()
    return {
        'status': 'OK',
        'user': UserSchema().dump(current_user)
    }


@bp.post("/logout")
@jwt_required(request)
@log_request
def logout():
    """Log out user."""
    # for cache control
    return {"status": "OK"}