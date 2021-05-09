"""DB api service."""

from nameko.rpc import rpc

from common.debug_tools import log_method
from common.constants import MAIN_ACCOUNT_NAME

from .db_translate import DBTranslate
from .db_handler import DBHandler


class DBService:
    """SQL alchemy based db handler class."""

    name = "db_service"
    handler = DBHandler()
    translate = DBTranslate()

    @rpc
    @log_method
    def create_user(self, name, password_hash):
        """Create new user object and get it back."""
        user = self.handler.create_user(name, password_hash)
        if user is None:
            return None
        account = self.handler.create_account(user.id, MAIN_ACCOUNT_NAME)
        self.handler.create_starting_labels(account.id)
        self.handler.create_starting_templates(account.id)
        return self.translate.m2s_user(user)

    @rpc
    @log_method
    def get_user(self, user_id=None, name=None):
        """Get user by id or name."""
        user = self.handler.get_user(user_id=user_id, name=name)
        return self.translate.m2s_user(user)

    @rpc
    @log_method
    def edit_user(self, user_id, name, password_hash):
        """Edit user in db."""
        user = self.handler.edit_user(user_id, name, password_hash)
        return self.translate.m2s_user(user)

    @rpc
    @log_method
    def create_account(self, name, user_id):
        """Create new account."""
        account = self.handler.create_account(name, user_id)
        return self.translate.m2s_account(account)

    @rpc
    @log_method
    def get_accounts(self, user_id):
        """Get account by id."""
        accounts = self.handler.get_accounts(user_id)
        if accounts is None:
            return None
        return [self.translate.m2s_account(account) for account in accounts]

    @rpc
    @log_method
    def edit_account(self, user_id, acc_id, name):
        """Edit account name."""
        account = self.handler.edit_account(user_id, acc_id, name)
        return self.translate.m2s_account(account)

    @rpc
    @log_method
    def delete_account(self, user_id, acc_id):
        """Delete account."""
        account = self.handler.delete_account(user_id, acc_id)
        return self.translate.m2s_account(account)

    @rpc
    @log_method
    def clear(self):
        """Clear all records."""
        self.handler.clear()
