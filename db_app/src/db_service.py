"""DB handler."""

from nameko.rpc import rpc

from common.schemas import UserSchema, AccountSchema
from common.debug_tools import log_method

from .db_translate import transform_return
from .models import session, AccountModel


class DBService:
    """SQL alchemy based db handler class."""

    name = "db_service"
    db = session

    @rpc
    @log_method
    @transform_return(AccountSchema)
    def create_account(self, user_id, account_name):
        """Create new account."""
        if self.db.query(AccountModel).filter(
            AccountModel.user_id == user_id,
            AccountModel.name == account_name
        ).first():
            return None
        account = AccountModel(
            user_id=user_id,
            name=account_name,
        )
        self.db.add(account)
        self.db.commit()
        return account

    @rpc
    @log_method
    @transform_return(AccountSchema)
    def get_accounts(self, user_id):
        """Get account from db by id."""
        accounts = self.db.query(AccountModel).filter(
            AccountModel.user_id == user_id
        )
        if accounts.count() == 0:
            return None
        return accounts.all()

    @rpc
    @log_method
    @transform_return(AccountSchema)
    def edit_account(self, user_id, acc_id, name):
        """Edit account name."""
        if self.db.query(AccountModel).filter(
            AccountModel.user_id == user_id,
            AccountModel.name == name
        ).first():
            return None
        account = self.db.query(AccountModel).filter(
            AccountModel.user_id == user_id,
            AccountModel.id == acc_id
        ).first()
        if not account:
            return None
        account.name = name
        self.db.commit()
        return account

    @rpc
    @log_method
    @transform_return(AccountSchema)
    def delete_account(self, user_id, acc_id):
        """Delete account."""
        account = self.db.query(AccountModel).filter(
            AccountModel.user_id == user_id,
            AccountModel.id == acc_id
        ).first()
        if not account:
            return None
        self.db.delete(account)
        self.db.commit()
        return account

    @rpc
    @log_method
    def clear(self):
        """Clear database."""
        account_count = self.db.query(AccountModel).delete()
        self.db.commit()
        return {
            'account': account_count,
        }
