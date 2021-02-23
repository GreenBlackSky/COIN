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
    def create_user(self, name, password_hash):
        """
        Create new user object and get it back.

        Also, create one account and current date.
        """
        db_user_data = self.handler.create_user(name, password_hash)
        if db_user_data is None:
            return {'status': 'user already exists'}
        return self.translate.user_model2schema(db_user_data)

    @rpc
    @log_method
    def check_user(self, name, password_hash):
        """Check user data and get id of ok."""
        user = self.handler.get_user(name=name)
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
        return self.translate.user_model2schema(user)

    # @rpc
    # @log_method
    # def create_account(self, user_id, name):
    #     pass

    # @rpc
    # @log_method
    # def get_account(self):
    #     pass

    # @rpc
    # @log_method
    # def edit_account(self):
    #     pass

    # @rpc
    # @log_method
    # def delete_account(self):
    #     pass

    @rpc
    @log_method
    def connection_test(self):
        """Test connection."""
        return 'ok'

    @rpc
    @log_method
    def test_set_value(self, value):
        """Test setting value."""
        return self.handler.test_set_date(value)

    @rpc
    @log_method
    def test_get_value(self, data_id):
        """Test getting value."""
        return self.test_get_value(self, data_id)

    @rpc
    @log_method
    def clear_users(self):
        """Clear all records."""
        self.handler.clear()
