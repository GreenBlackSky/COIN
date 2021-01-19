"""Redis-based cache for app data."""

import logging
from functools import wraps

from nameko.rpc import rpc
from nameko_redis import Redis


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


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    redis = Redis('redis')

    @rpc
    @log_method
    def connection_test(self):
        """Test connection."""
        return 'ok'

    @rpc
    @log_method
    def test_set_value(self, key, value):
        """Test setting value."""
        self.redis.set(key, value)

    @rpc
    @log_method
    def test_get_value(self, key):
        """Test getting value."""
        value = self.redis.get(key)
        return value

    @rpc
    @log_method
    def get_user_by_name(self, name):
        """Get user from db service by name and cache it in redis."""
        user_id = self.redis.hget('user_id', name)
        if user_id is not None:
            user = self.redis.hget('user', user_id)
        else:
            user = rpc.db_service.get_user_by_name(name)
            if user is not None:
                self.redis.hset('user_id', user.name)
                self.redis.hset('user', user)
        return user

    @rpc
    @log_method
    def get_user(self, user_id):
        """Get user from db service and cache it."""
        user = self.redis.hget('user', user_id)
        if user is None:
            user = rpc.db_service.get_user(user_id)
            if user is not None:
                self.redis.hset('user_id', user.name)
                self.redis.hset('user', user)
        return user
