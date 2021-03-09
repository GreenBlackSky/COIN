"""DB api service."""

from nameko.rpc import rpc

from common.debug_tools import log_method
from .db_translate import DBTranslate
from .db_handler import DBHandler


class DBService:
    """SQL alchemy based db handler class."""

    name = "db_service"
    handler = DBHandler()
    translate = DBTranslate()

    @rpc
    @log_method
    def create_user(self, name, email, password_hash):
        """Create new user object and get it back."""
        user = self.handler.create_user(name, email, password_hash)
        if user is None:
            return None
        return self.translate.user_model2schema(user, [])

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
    def get_user(self, user_id):
        """Get user by id."""
        user = self.handler.get_user(user_id=user_id)
        if user is None:
            return {'status': 'no such user'}
        return self.translate.user_model2schema(user, [])

    @rpc
    @log_method
    def edit_user(self, user_id, field, value):
        """Edit user in db."""
        self.handler.update_user(user_id, field, value, True)

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
    def connection_test(self):
        """Test connection."""
        return 'ok'

    @rpc
    @log_method
    def test_set_value(self, value):
        """Test setting value."""
        return self.handler.test_set_value(value)

    @rpc
    @log_method
    def test_get_value(self, data_id):
        """Test getting value."""
        return self.handler.test_get_value(data_id)

    @rpc
    @log_method
    def clear_users(self):
        """Clear all records."""
        self.handler.clear()
