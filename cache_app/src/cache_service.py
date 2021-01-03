"""Redis-based cache for app data."""

import logging

from nameko.rpc import rpc
from nameko_redis import Redis


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    redis = Redis('redis')

    @rpc
    def simple_test(self):
        logging.debug('simple_test')
        return 'simple'

    @rpc
    def test_set_value(self, key, value):
        logging.debug(f"test_set_value setting {key} : {value}")
        self.redis.set(key, value)
        logging.debug(f"test_set_value set {key} : {value}")

    @rpc
    def test_get_value(self, key):
        logging.debug(f"test_get_value getting {key}")
        value = self.redis.get(key)
        logging.debug(f"test_get_value got {key} : {value}")
        return value
