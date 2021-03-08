"""Module contains app web."""

import logging
from functools import wraps

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_current_user

from . import rpc
from common.debug_tools import log_request
from common.schemas import AccountSchema
from common.constants import ENTITY
from .api_app_common import parse_request


bp = Blueprint('account_bp', __name__)


@bp.route("/create_account", methods=['POST'])
@log_request
@jwt_required()
def create_account():
    """Create new account."""
    try:
        name, is_main = parse_request(request, ('name', 'is_main'))
    except Exception as e:
        return {'status': str(e)}

    account = rpc.db_service.create_account(
        get_current_user().id,
        name,
        is_main
    )
    if account is None:
        return {'status': 'account already exist'}
    account = AccountSchema().load(account)
    return {'status': 'OK', 'account_id': account.id}


@bp.route("/get_account", methods=['POST'])
@log_request
@jwt_required()
def get_account():
    """Get existing account by ID."""
    try:
        account_id = parse_request(request, 'account_id')
    except Exception as e:
        return {'status': str(e)}

    account = rpc.cache_service.get(ENTITY.ACCOUNT, account_id)
    if account is None:
        return {'status': 'no such account'}
    return {'status': 'OK', 'account': account}


@bp.route("/edit_account", methods=['POST'])
@log_request
@jwt_required()
def edit_account():
    """Edit account."""
    pass


@bp.route("/delete_account", methods=['POST'])
@log_request
@jwt_required()
def delete_account():
    """Get existing account by ID."""
    pass
