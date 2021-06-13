"""Flask blueprint, that contains accounts manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import log_request
from common.interfaces import AccountService

from ..request_helpers import parse_request_args


bp = Blueprint('account_bp', __name__)


@bp.post("/create_account")
@jwt_required()
@log_request(request)
def create_account():
    """Request creating new account."""
    (name,), _ = parse_request_args(request, ('name',))
    return AccountService.create_account(user_id=current_user.id, name=name)


@bp.post("/get_accounts")
@jwt_required()
@log_request(request)
def get_accounts():
    """Get account from db by id."""
    return AccountService.get_accounts(user_id=current_user.id)


@bp.post("/edit_account")
@jwt_required()
@log_request(request)
def edit_account():
    """Request to edit account."""
    (account_id, name), _ = parse_request_args(request, ('id', 'name'))
    return AccountService.edit_account(
        user_id=current_user.id,
        account_id=account_id,
        name=name
    )


@bp.post("/delete_account")
@jwt_required()
@log_request(request)
def delete_account():
    """Delete existing account."""
    (account_id,), _ = parse_request_args(request, ('id',))
    return AccountService.delete_account(
        user_id=current_user.id,
        account_id=account_id
    )
