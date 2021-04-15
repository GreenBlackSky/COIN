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
    def create_user(self, email, password_hash):
        """Create new user object and get it back."""
        user = self.handler.create_user(email, password_hash)
        if user is None:
            return None
        account = self.handler.create_account(user.id, MAIN_ACCOUNT_NAME, True)
        self.handler.create_starting_categories(account.id)
        self.handler.create_starting_templates(account.id)
        return self.translate.m2s_user(user)

    @rpc
    @log_method
    def get_user(self, user_id=None, email=None):
        """Get user by id or email."""
        user = self.handler.get_user(user_id=user_id, email=email)
        if user is None:
            return None
        return self.translate.m2s_user(user)

    @rpc
    @log_method
    def update_user(self, user_id, email, password_hash):
        """Edit user in db."""
        user = self.handler.update_user(user_id, email, password_hash)
        if user is None:
            return None
        return self.translate.m2s_user(user)

    @rpc
    @log_method
    def create_account(self, user_id, name):
        """Create new account."""
        account = self.handler.create_account(user_id, name)
        return self.translate.m2s_account(account)

    @rpc
    @log_method
    def get_account(self, account_id):
        """Get account by id."""
        account = self.handler.get_account(account_id)
        if account is None:
            return None
        return self.translate.m2s_account(account)

    @rpc
    @log_method
    def edit_account(self, acc_id, name):
        pass

    @rpc
    @log_method
    def delete_account(self, acc_id):
        pass

    @rpc
    @log_method
    def clear(self):
        """Clear all records."""
        self.handler.clear()
