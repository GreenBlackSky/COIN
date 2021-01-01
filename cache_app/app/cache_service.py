"""Redis-based cache for app data."""

from nameko.rpc import rpc
# from nameko_redis import Redis


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    # redis = Redis('development')

    @rpc
    def set_test_value(self, key, value):
        """Set test value."""
        # self.redis.set(key, value)

    @rpc
    def get_test_value(self, key):
        """Get test value."""
        return 10
        # return self.redis.get(key)