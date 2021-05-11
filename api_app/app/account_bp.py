"""Flask blueprint, that contains accounts manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import wrap_request
from common.constants import MAX_ACCOUNTS

from . import rpc


bp = Blueprint('account_bp', __name__)


@bp.route("/create_account", methods=['POST'])
@jwt_required()
@wrap_request('name')
def create_account(name):
    """Request to create new account."""
    accounts = rpc.db_service.get_accounts(current_user.id)
    if len(accounts) >= MAX_ACCOUNTS:
        return {'status': 'max accounts'}

    account = rpc.db_service.create_account(name, current_user.id)
    if account is None:
        return {'status': "account already exists"}

    return {'status': 'OK', 'account': account}


@bp.route("/get_accounts", methods=['POST'])
@jwt_required()
@wrap_request()
def get_accounts():
    """Get all accounts user has."""
    return {
        'status': 'OK',
        'accounts': rpc.db_service.get_accounts(current_user.id)
    }


@bp.route("/edit_account", methods=['POST'])
@jwt_required()
@wrap_request('id', 'name')
def edit_account(acc_id, name):
    """Request to create new account."""
    accounts = rpc.db_service.get_accounts(current_user.id)
    if not any(account['id'] == acc_id for account in accounts):
        return {'status': "no such account"}
    if any(account['name'] == name for account in accounts):
        return {'status': "account already exists"}

    account = rpc.db_service.edit_account(current_user.id, acc_id, name)
    return {'status': 'OK', 'account': account}


@bp.route("/delete_account", methods=['POST'])
@jwt_required()
@wrap_request('id')
def delete_account(acc_id):
    """Delete existing account."""
    accounts = rpc.db_service.get_accounts(current_user.id)
    if len(accounts) == 1:
        return {'status': "can't delete the only account"}
    if not any(account['id'] == acc_id for account in accounts):
        return {'status': "no such account"}

    account = rpc.db_service.delete_account(current_user.id, acc_id)
    return {'status': 'OK', 'account': account}
