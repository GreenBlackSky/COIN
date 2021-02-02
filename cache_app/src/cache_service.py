"""Redis-based cache for app data."""

import logging
from functools import wraps

from nameko.rpc import rpc
from nameko_redis import Redis

from .schemas import UserSchema, User


def log_method(method):
    """Decorate method to log its input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        logging.debug(f"start {method.__name__}")
        ret = method(*args, **kargs)
        logging.debug(f"finish {method.__name__}")
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

    def _get_user_from_cache(self, user_id):
        user = self.redis.hget('user', user_id)
        if user is None:
            return None
        return UserSchema().loads(user)

    def _get_user_from_db(self, user_id):
        user = rpc.db_service.get_user(user_id)
        if user is None:
            return None
        return UserSchema().load(user)

    @rpc
    @log_method
    def get_user(self, user_id):
        """Get user from db service and cache it."""
        user = self._get_user_from_cache(user_id)
        if user is None:
            user = self._get_user_from_db(user_id)
        if user is None:
            return None
        self.redis.hset('user', user.id, UserSchema().dumps(user))
        return UserSchema().dump(user)

    @rpc
    @log_method
    def clear(self):
        """Clear cache."""
        self.redis.flushdb()
