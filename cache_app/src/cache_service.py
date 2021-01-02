"""Redis-based cache for app data."""

import logging

from nameko.rpc import rpc
# from nameko_redis import Redis


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    # redis = Redis('development')

    @rpc
    def simple_test(self):
        logging.debug('simple_test')
        return 'simple'

    @rpc
    def set_test_value(self, key, value):
        pass
        # self.redis.set(key, value)

    @rpc
    def get_test_value(self, key):
        pass
        # return self.redis.get(key)
