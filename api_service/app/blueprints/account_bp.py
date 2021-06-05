"""Flask blueprint, that contains accounts manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.constants import MAX_ACCOUNTS
from common.debug_tools import log_function, log_method, log_request
from common.schemas import AccountSchema

from ..request_helpers import parse_request_args
from ..model import session, AccountModel


bp = Blueprint('account_bp', __name__)


@bp.post("/create_account")
@jwt_required()
@parse_request_args(request, ('name',))
@log_request
def create_account_view(name):
    return create_account(current_user.id, name)


@log_function
def create_account(user_id, name):
    """Create new account."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == user_id
    )
    if accounts.count() >= MAX_ACCOUNTS:
        return {'status': 'max accounts'}

    if session.query(AccountModel).filter(
        AccountModel.user_id == user_id,
        AccountModel.name == name
    ).first():
        return {'status': "account already exists"}
    account = AccountModel(
        user_id=user_id,
        name=name,
    )
    session.add(account)
    session.commit()
    return {'status': 'OK', 'account': AccountSchema().dump(account)}


@bp.post("/get_accounts")
@jwt_required()
@parse_request_args(request)
@log_request
def get_accounts():
    """Get account from db by id."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id
    )
    if accounts.count() == 0:
        return {'status': 'no accounts with given user_id'}

    schema = AccountSchema()
    return {
        'status': 'OK',
        'accounts': [schema.dump(acc) for acc in accounts.all()]
    }


@bp.post("/edit_account")
@jwt_required()
@parse_request_args(request, ('id', 'name'))
@log_request
def edit_account(acc_id, name):
    """Request to edit account."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id,
        AccountModel.id == acc_id
    )
    if accounts.count() == 0:
        return {'status': "no such account"}

    if session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id,
        AccountModel.name == name,
        AccountModel.id != acc_id
    ).count() != 0:
        return {'status': "account already exists"}

    account = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id,
        AccountModel.id == acc_id
    ).first()
    account.name = name
    session.commit()
    return {'status': 'OK', 'account': AccountSchema().dump(account)}


@bp.post("/delete_account")
@jwt_required()
@parse_request_args(request, ('id',))
@log_request
def delete_account(acc_id):
    """Delete existing account."""
    account = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id,
        AccountModel.id == acc_id
    ).first()
    if account is None:
        return {'status': "no such account"}

    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id,
    )
    if accounts.count() == 1:
        return {'status': "can't delete the only account"}

    session.delete(account)
    session.commit()
    return {'status': 'OK', 'account': AccountSchema().dump(account)}
