"""Flask blueprint, that contains accounts manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.celery_holder import celery_app
from common.debug_tools import log_request

from ..request_helpers import parse_request_args


bp = Blueprint('account_bp', __name__)


@bp.post("/create_account")
@jwt_required()
@parse_request_args(request, ('name',))
@log_request
def create_account_view(name):
    """Request creating new account."""
    return celery_app.send_task(
        'app.handlers.account.create_account',
        kwargs={'user_id': current_user.id, 'name': name}
    ).get()


@bp.post("/get_accounts")
@jwt_required()
@parse_request_args(request)
@log_request
def get_accounts():
    """Get account from db by id."""
    return celery_app.send_task(
        'app.handlers.account.get_accounts',
        kwargs={'user_id': current_user.id}
    ).get()


@bp.post("/edit_account")
@jwt_required()
@parse_request_args(request, ('id', 'name'))
@log_request
def edit_account(acc_id, name):
    """Request to edit account."""
    return celery_app.send_task(
        'app.handlers.account.edit_account',
        kwargs={'user_id': current_user.id, 'acc_id': acc_id, 'name': name}
    ).get()


@bp.post("/delete_account")
@jwt_required()
@parse_request_args(request, ('id',))
@log_request
def delete_account(acc_id):
    """Delete existing account."""
    return celery_app.send_task(
        'app.handlers.account.delete_account',
        kwargs={'user_id': current_user.id, 'acc_id': acc_id}
    ).get()
