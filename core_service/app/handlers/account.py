"""Module contains accounts manipulation methods."""

from celery_abc import WorkerMetaBase

from common.celery_utils import celery_app
from common.constants import MAX_ACCOUNTS, STARTING_CATEGORIES
from common.interfaces import AccountService
from common.schemas import AccountSchema

from ..model import CategoryModel, SavePointModel, session, AccountModel


account_schema = AccountSchema()


class AccountHandler(AccountService, metaclass=WorkerMetaBase):
    """Class contains method for handling account stuff."""

    def create_account(self, user_id, name):
        """Create new account."""
        accounts = session\
            .query(AccountModel)\
            .filter(AccountModel.user_id == user_id)
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

        categories = [
            CategoryModel(user_id=user_id, account_id=account.id, **category)
            for category in STARTING_CATEGORIES
        ]
        session.add_all(categories)
        session.commit()

        return {'status': 'OK', 'account': account_schema.dump(account)}

    def get_accounts(self, user_id):
        """Get account from db by id."""
        accounts = session.query(AccountModel).filter(
            AccountModel.user_id == user_id
        )
        if accounts.count() == 0:
            return {'status': 'no accounts with given user_id'}

        return {
            'status': 'OK',
            'accounts': [account_schema.dump(acc) for acc in accounts.all()]
        }

    def edit_account(self, user_id, account_id, name):
        """Request to edit account."""
        account = session.get(AccountModel, account_id)
        if account is None:
            return {'status': "no such account"}

        if account.user_id != user_id:
            return {'status': 'accessing account of another user'}

        if session.query(AccountModel).filter(
            AccountModel.user_id == user_id,
            AccountModel.name == name,
            AccountModel.id != account_id
        ).count() != 0:
            return {'status': "account already exists"}

        account.name = name
        session.commit()
        return {'status': 'OK', 'account': account_schema.dump(account)}

    def delete_account(self, user_id, account_id):
        """Delete existing account."""
        accounts = session.query(AccountModel).filter(
            AccountModel.user_id == user_id,
        )
        if accounts.count() == 1:
            return {'status': "can't delete the only account"}

        account = session.get(AccountModel, account_id)
        if account is None:
            return {'status': "no such account"}

        if account.user_id != user_id:
            return {'status': 'accessing account of another user'}

        session\
            .query(SavePointModel)\
            .filter(SavePointModel.account_id == account.id)\
            .delete()
        session.delete(account)
        session.commit()
        return {'status': 'OK', 'account': account_schema.dump(account)}

    def clear_accounts(self):
        """Clear all accounts from db."""
        account_count = session.query(AccountModel).delete()
        return account_count

    def check_account_user(self, account_id, user_id):
        """Check if account belongs to user."""
        accounts_response = AccountHandler.get_accounts(user_id)
        if accounts_response['status'] != 'OK':
            return accounts_response
        if not any(
            user_acc['id'] == account_id
            for user_acc in accounts_response['accounts']
        ):
            return {'status': 'no such account'}
        return {'status': 'OK'}


AccountHandler(celery_app)
