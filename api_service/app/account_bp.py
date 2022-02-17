"""Flask blueprint, that contains accounts manipulation methods."""

from functools import wraps

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from .constants import MAX_ACCOUNTS, STARTING_CATEGORIES
from .debug_tools import log_request
from .model import session, AccountModel, CategoryModel, SavePointModel
from .request_helpers import parse_request_args
from .schemas import AccountSchema


bp = Blueprint("account_bp", __name__)
account_schema = AccountSchema()


def create_account(user_id, name):
    """Create new account."""
    account = AccountModel(
        user_id=user_id,
        name=name,
    )
    session.add(account)
    session.commit()

    categories = [
        CategoryModel(
            user_id=user_id, account_id=account.id, **category
        )
        for category in STARTING_CATEGORIES
    ]
    session.add_all(categories)
    session.commit()
    return account


@bp.post("/create_account")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def create_account_endpoint(name):
    """Request creating new account."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id
    )
    if accounts.count() >= MAX_ACCOUNTS:
        return {"status": "max accounts"}
    if (
        session.query(AccountModel)
        .filter(
            AccountModel.user_id == current_user.id, AccountModel.name == name
        )
        .first()
    ):
        return {"status": "account already exists"}
    return {
        "status": "OK",
        "account": account_schema.dump(create_account(current_user.id, name)),
    }


def get_accounts(user_id):
    """Get all users accounts."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == user_id
    )
    return [account_schema.dump(acc) for acc in accounts.all()]


@bp.post("/get_accounts")
@jwt_required()
@log_request(request, current_user)
def get_accounts_endpoint():
    """Web endpoint for getting accounts of user."""
    accounts = get_accounts(current_user.id)
    if not accounts:
        return {"status": "no accounts with given user_id"}

    return {
        "status": "OK",
        "accounts": accounts,
    }


@bp.post("/edit_account")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def edit_account(account_id, name):
    """Request to edit account."""
    account = session.get(AccountModel, account_id)
    if account is None:
        return {"status": "no such account"}

    if account.user_id != current_user.id:
        return {"status": "accessing account of another user"}

    if (
        session.query(AccountModel)
        .filter(
            AccountModel.user_id == current_user.id,
            AccountModel.name == name,
            AccountModel.id != account_id,
        )
        .count()
        != 0
    ):
        return {"status": "account already exists"}

    account.name = name
    session.commit()
    return {"status": "OK", "account": account_schema.dump(account)}


@bp.post("/delete_account")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def delete_account(account_id):
    """Delete existing account."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == current_user.id,
    )
    if accounts.count() == 1:
        return {"status": "can't delete the only account"}

    account = session.get(AccountModel, account_id)
    if account is None:
        return {"status": "no such account"}

    if account.user_id != current_user.id:
        return {"status": "accessing account of another user"}

    session.query(SavePointModel).filter(
        SavePointModel.account_id == account.id
    ).delete()
    session.delete(account)
    session.commit()
    return {"status": "OK", "account": account_schema.dump(account)}


def account_belongs_to_user(account_id, user_id):
    """Check if account belongs to user."""
    return any(
        user_acc["id"] == account_id for user_acc in get_accounts(user_id)
    )


def check_account(endpoint):
    @wraps(endpoint)
    def _wrapper(account_id, *args, **kvargs):
        if not account_belongs_to_user(account_id, current_user.id):
            return {"status": "Invalid account"}
        return endpoint(account_id, *args, **kvargs)

    return _wrapper
