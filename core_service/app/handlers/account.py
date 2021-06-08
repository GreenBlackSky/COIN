"""Module contains accounts manipulation methods."""

from common.celery_utils import celery_app
from common.constants import MAX_ACCOUNTS
from common.debug_tools import log_function
from common.schemas import AccountSchema

from ..model import session, AccountModel


@celery_app.task
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


@celery_app.task
@log_function
def get_accounts(user_id):
    """Get account from db by id."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == user_id
    )
    if accounts.count() == 0:
        return {'status': 'no accounts with given user_id'}

    schema = AccountSchema()
    return {
        'status': 'OK',
        'accounts': [schema.dump(acc) for acc in accounts.all()]
    }


@celery_app.task
@log_function
def edit_account(user_id, acc_id, name):
    """Request to edit account."""
    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == user_id,
        AccountModel.id == acc_id
    )
    if accounts.count() == 0:
        return {'status': "no such account"}

    if session.query(AccountModel).filter(
        AccountModel.user_id == user_id,
        AccountModel.name == name,
        AccountModel.id != acc_id
    ).count() != 0:
        return {'status': "account already exists"}

    account = session.query(AccountModel).filter(
        AccountModel.user_id == user_id,
        AccountModel.id == acc_id
    ).first()
    account.name = name
    session.commit()
    return {'status': 'OK', 'account': AccountSchema().dump(account)}


@celery_app.task
@log_function
def delete_account(user_id, acc_id):
    """Delete existing account."""
    account = session.query(AccountModel).filter(
        AccountModel.user_id == user_id,
        AccountModel.id == acc_id
    ).first()
    if account is None:
        return {'status': "no such account"}

    accounts = session.query(AccountModel).filter(
        AccountModel.user_id == user_id,
    )
    if accounts.count() == 1:
        return {'status': "can't delete the only account"}

    session.delete(account)
    session.commit()
    return {'status': 'OK', 'account': AccountSchema().dump(account)}


@log_function
@celery_app.task
def clear_accounts():
    """Clear all accounts from db and clear cache."""
    account_count = session.query(AccountModel).delete()
    return account_count
