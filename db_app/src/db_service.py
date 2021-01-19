"""Postgres based data base handler service."""

import logging
from functools import wraps

from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession
from .models import DeclarativeBase, TestData, User


def log_method(method):
    """Decorate method to log its input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        print_args = [arg for arg in args if arg is not method.__self__]
        logging.debug(f"start {method.__name__} with {str(print_args)}")
        ret = method(*args, **kargs)
        logging.debug(
            f"finish {method.__name__} with {str(print_args)}, {str(ret)}"
        )
        return ret
    return _wrapper


class DBService:
    """SQL alchemy based db handler class."""

    name = "db_service"
    db = DatabaseSession(DeclarativeBase)

    @rpc
    @log_method
    def connection_test(self):
        """Test connection."""
        return 'ok'

    @rpc
    @log_method
    def test_set_value(self, value):
        """Test setting value."""
        data = TestData(value=value)
        self.db.add(data)
        self.db.commit()
        return data.id

    @rpc
    @log_method
    def test_get_value(self, data_id):
        """Test getting value."""
        data = self.db.query(TestData).get(data_id)
        return data.value if data else None

    @rpc
    @log_method
    def create_user(self, name, password_hash):
        """Create new user object and get it back."""
        user = self.db.query(User).filter_by(name=name).first()
        if user:
            return None
        user = User(name=name, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        return user

    @rpc
    @log_method
    def get_user_by_name(self, name):
        """Get user by name."""
        return self.db.query(User).filter_by(name=name).first()

    @rpc
    @log_method
    def get_user(self, user_id):
        """Get user by id."""
        return self.db.query(User).get(user_id)
