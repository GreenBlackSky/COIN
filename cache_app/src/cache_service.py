"""Redis-based cache for app data."""

from typing import Optional

from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis

from common.debug_tools import log_method
from common.schemas import UserSchema, AccountSchema, \
    CategorySchema, TemplateSchema, DateSchema, EventSchema


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    redis = Redis('redis')
    db_service = RpcProxy('db_service')

    def __init__(self):
        """Init service."""
        self.entities = {
            'user': (UserSchema(), 'get_user'),
            'account': (AccountSchema(), 'get_account'),
            'category': (CategorySchema(), 'get_category'),
            'template': (TemplateSchema(), 'get_template'),
            'date': (DateSchema(), 'get_date'),
            'event': (EventSchema(), 'get_event'),
        }

    @log_method
    def _cache_stuff(self, stuff_id, section):
        schema, method_name = self.entities[section]
        stuff_raw = self.redis.hget(section, stuff_id)
        if stuff_raw is None:
            stuff_raw = getattr(self.db_service, method_name)(stuff_id)
            if stuff_raw is None:
                return None
            else:
                stuff = schema.load(stuff_raw)
                self.redis.hset(section, stuff_id, schema.dumps(stuff))
        else:
            stuff = schema.loads(json_data=stuff_raw)
        return schema.dump(stuff)

    @rpc
    @log_method
    def get_user(self, user_id):
        """Get user from db service and cache it."""
        return self._cache_stuff(user_id, 'user')

    @rpc
    @log_method
    def get_account(self, account_id):
        """Get account from db service and cache it."""
        return self._cache_stuff(account_id, 'account')

    @rpc
    @log_method
    def forget_account(self, account_id):
        """Remove account from cache."""
        self.redis.hdel('account', account_id)

    @rpc
    @log_method
    def forget_user(self, user_id):
        """Remove user from cache."""
        self.redis.hdel('user', user_id)

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
    def clear(self):
        """Clear cache."""
        self.redis.flushdb()
