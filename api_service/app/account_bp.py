"""Flask blueprint, that contains accounts manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import wrap_request

from . import rpc


bp = Blueprint('account_bp', __name__)


@bp.route("/create_account", methods=['POST'])
@jwt_required()
@wrap_request('name')
def create_account(name):
    """Request to create new account."""
    return rpc.account_service.create_account(current_user.id, name)


@bp.route("/get_accounts", methods=['POST'])
@jwt_required()
@wrap_request()
def get_accounts():
    """Get all accounts user has."""
    return rpc.account_service.get_accounts(current_user.id)


@bp.route("/edit_account", methods=['POST'])
@jwt_required()
@wrap_request('id', 'name')
def edit_account(acc_id, name):
    """Request to create new account."""
    return rpc.account_service.edit_account(current_user.id, acc_id, name)


@bp.route("/delete_account", methods=['POST'])
@jwt_required()
@wrap_request('id')
def delete_account(acc_id):
    """Delete existing account."""
    return rpc.account_service.delete_account(current_user.id, acc_id)
