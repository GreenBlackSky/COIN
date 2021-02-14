"""Redis-based cache for app data."""

from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis

from common.debug_tools import log_method
from common.schemas import UserSchema


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    redis = Redis('redis')
    db_service = RpcProxy('db_service')

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
    def get_user(self, user_id):
        """Get user from db service and cache it."""
        user = self.redis.hget('user', user_id)
        if user is None:
            user = self.db_service.get_user(user_id)
            if user is None:
                return None
            else:
                user = UserSchema().load(user)
                self.redis.hset('user', user.id, UserSchema().dumps(user))
        else:
            user = UserSchema().loads(user)
        return UserSchema().dump(user)

    @rpc
    @log_method
    def forget_user(self, user_id):
        self.redis.hdel('user', user_id)

    @rpc
    @log_method
    def clear(self):
        """Clear cache."""
        self.redis.flushdb()
