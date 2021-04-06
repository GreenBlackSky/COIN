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
        account = self.handler.create_account(
            user.id,
            MAIN_ACCOUNT_NAME,
            True,
            True
        )
        return self.translate.user_model2schema(user, [account])

    @rpc
    @log_method
    def check_user(self, email, password_hash):
        """Check user data and get id of ok."""
        user = self.handler.get_user(email=email)
        if user is None:
            return {'status': 'no such user'}
        if user.password_hash != password_hash:
            return {'status': 'wrong password'}
        return {'status': 'OK', 'user_id': user.id}

    @rpc
    @log_method
    def check_email(self, email):
        """Check if email is already taken."""
        user = self.handler.get_user(email=email)
        if user is not None:
            return {'status': 'user exists'}
        return {'status': 'OK'}

    @rpc
    @log_method
    def get_user(self, user_id):
        """Get user by id."""
        user = self.handler.get_user(user_id=user_id)
        if user is None:
            return {'status': 'no such user'}
        return self.translate.user_model2schema(user, [])

    @rpc
    @log_method
    def edit_user_data(self, user_id, email, password_hash):
        """Edit user in db."""
        user = self.handler.update_user(
            user_id, email, password_hash, True
        )
        if user is None:
            return {'status': 'no such user'}
        return {
            'status': 'OK',
            'user': self.translate.user_model2schema(user, [])
        }

    @rpc
    @log_method
    def create_account(self, user_id, name):
        """Create new account."""
        account = self.handler.create_account(user_id, name)
        return self.translate.account_model2Schema(account, [], [], [])

    @rpc
    @log_method
    def get_account(self, account_id):
        """Get account by id."""
        account = self.handler.get_account(account_id)
        if account is None:
            return {'status': 'no such account'}
        return self.translate.account_model2Schema(account, [], [], [])

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
    def clear_users(self):
        """Clear all records."""
        self.handler.clear()
