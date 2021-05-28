"""Core logic service."""

from hashlib import md5

from nameko.rpc import rpc, RpcProxy

from common.schemas import UserSchema
from common.debug_tools import log_method
from common.constants import MAX_ACCOUNTS, MAIN_ACCOUNT_NAME


class CoreService:
    """Class contains core logic of app."""

    name = "core_service"
    db_service = RpcProxy('db_service')

    @rpc
    @log_method
    def create_account(self, user_id, name):
        """Create new account."""
        accounts = self.db_service.get_accounts(user_id)
        if len(accounts) >= MAX_ACCOUNTS:
            return {'status': 'max accounts'}

        account = self.db_service.create_account(user_id, name)
        if account is None:
            return {'status': "account already exists"}

        return {'status': 'OK', 'account': account}

    @rpc
    @log_method
    def edit_account(self, user_id, acc_id, name):
        """Edit account name."""
        accounts = self.db_service.get_accounts(user_id)
        if not any(account['id'] == acc_id for account in accounts):
            return {'status': "no such account"}
        if any(account['name'] == name for account in accounts):
            return {'status': "account already exists"}

        account = self.db_service.edit_account(user_id, acc_id, name)
        return {'status': 'OK', 'account': account}

    @rpc
    @log_method
    def delete_account(self, user_id, acc_id):
        """Delete account."""
        accounts = self.db_service.get_accounts(user_id)
        if len(accounts) == 1:
            return {'status': "can't delete the only account"}
        if not any(account['id'] == acc_id for account in accounts):
            return {'status': "no such account"}

        account = self.db_service.delete_account(user_id, acc_id)
        return {'status': 'OK', 'account': account}
