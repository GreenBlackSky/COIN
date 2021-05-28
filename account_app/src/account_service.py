"""Account logic service."""

from common.schemas import AccountSchema
from nameko.rpc import rpc

from common.debug_tools import log_method
from common.constants import MAX_ACCOUNTS

from .model import session, AccountModel


class AccountsService:
    """Class contains logic that concerns accounts."""

    name = "account_service"

    @rpc
    @log_method
    def create_account(self, user_id, account_name):
        """Create new account."""
        accounts = session.query(AccountModel).filter(
            AccountModel.user_id == user_id
        )
        if accounts.count() >= MAX_ACCOUNTS:
            return {'status': 'max accounts'}

        if session.query(AccountModel).filter(
            AccountModel.user_id == user_id,
            AccountModel.name == account_name
        ).first():
            return {'status': "account already exists"}
        account = AccountModel(
            user_id=user_id,
            name=account_name,
        )
        session.add(account)
        session.commit()
        return {'status': 'OK', 'account': AccountModel().dump(account)}

    @rpc
    @log_method
    def get_accounts(self, user_id):
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

    @rpc
    @log_method
    def edit_account(self, user_id, acc_id, name):
        """Edit account name."""
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
        self.db.commit()
        return {'status': 'OK', 'account': AccountSchema().dump(account)}

    @rpc
    @log_method
    def delete_account(self, user_id, acc_id):
        """Delete account."""
        account = session.query(AccountModel).filter(
            AccountModel.user_id == user_id,
            AccountModel.id == acc_id
        ).first()
        if not account:
            return {'status': "no such account"}

        session.delete(account)
        session.commit()
        return {'status': 'OK', 'account': account}

    @rpc
    @log_method
    def clear(self):
        """Clear database."""
        account_count = session.query(AccountModel).delete()
        session.commit()
        return {
            'account': account_count,
        }
