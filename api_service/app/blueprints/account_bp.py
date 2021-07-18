"""Flask blueprint, that contains accounts manipulation methods."""

from celery_abc import CallerMetaBase
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.celery_utils import celery_app
from common.debug_tools import log_request
from common.interfaces import AccountService

from ..request_helpers import parse_request_args


class AccountCaller(AccountService, metaclass=CallerMetaBase):
    pass


bp = Blueprint('account_bp', __name__)
accountService = AccountCaller(celery_app)


@bp.post("/create_account")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def create_account(name):
    """Request creating new account."""
    return accountService.create_account(user_id=current_user.id, name=name)


@bp.post("/get_accounts")
@jwt_required()
@log_request(request, current_user)
def get_accounts():
    """Get account from db by id."""
    return accountService.get_accounts(user_id=current_user.id)


@bp.post("/edit_account")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def edit_account(account_id, name):
    """Request to edit account."""
    return accountService.edit_account(
        user_id=current_user.id,
        account_id=account_id,
        name=name
    )


@bp.post("/delete_account")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def delete_account(account_id):
    """Delete existing account."""
    return accountService.delete_account(
        user_id=current_user.id,
        account_id=account_id
    )
