"""Module contains accounts manipulation methods."""

from common.constants import MAX_ACCOUNTS
from common.interfaces import AccountService
from common.schemas import AccountSchema

from ..model import session, AccountModel


account_schema = AccountSchema()


class AccountHandler(AccountService):
    """
    Class contains method for handling account stuff.

    Do no instantiate.
    """

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
        # TODO create first savepoint
        session.commit()
        return {'status': 'OK', 'account': account_schema.dump(account)}

    def get_accounts(user_id):
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

    def edit_account(user_id, account_id, name):
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

    def delete_account(user_id, account_id):
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

        session.delete(account)
        # TODO delete all savepoints
        session.commit()
        return {'status': 'OK', 'account': account_schema.dump(account)}

    def clear_accounts():
        """Clear all accounts from db."""
        account_count = session.query(AccountModel).delete()
        return account_count
