"""Redis-based cache for app data."""

import logging
from functools import wraps

from nameko.rpc import rpc
from nameko_redis import Redis


def log_method(method):
    @wraps(method)
    def _wrapper(*args, **kargs):
        print_args = [arg for arg in args if arg is not method.__self__]
        logging.debug(f"start {method.__name__} with {str(print_args)}, {str(kargs)}")
        ret = method(*args, **kargs)
        logging.debug(f"finish {method.__name__} with {str(print_args)}, {str(kargs)}, {str(ret)}")
        return ret
    return _wrapper


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    redis = Redis('redis')

    @rpc
    @log_method
    def connection_test(self):
        return 'ok'

    @rpc
    @log_method
    def test_set_value(self, key, value):
        self.redis.set(key, value)

    @rpc
    @log_method
    def test_get_value(self, key):
        value = self.redis.get(key)
        return value

    @rpc
    @log_method
    def get_user(user_id):
        pass
