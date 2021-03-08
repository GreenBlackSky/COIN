"""Redis-based cache for app data."""

from typing import Optional

from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis

from common.debug_tools import log_method
from common.schemas import UserSchema, AccountSchema, \
    CategorySchema, TemplateSchema, DateSchema, EventSchema
from common.constants import ENTITY, ENTITY_SCHEMAS


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    redis = Redis('redis')
    db_service = RpcProxy('db_service')

    def __init__(self):
        """Init service."""

    @rpc
    @log_method
    def get(self, entity_type, entity_id):
        """Get some stuff from cache or db."""
        schema = ENTITY_SCHEMAS[entity_type]
        entity_raw = self.redis.hget(entity_type, entity_id)
        if entity_raw is None:
            entity_raw = getattr(
                self.db_service, f'get_{entity_type}'
            )(entity_id)
            if entity_raw is None:
                return None
            else:
                stuff = schema.load(entity_raw)
                self.redis.hset(entity_type, entity_id, schema.dumps(stuff))
        else:
            stuff = schema.loads(json_data=entity_raw)
        return schema.dump(stuff)

    @rpc
    @log_method
    def forget(self, entity_type, entity_id):
        """Remove stuff from cache."""
        self.redis.hdel(entity_type, entity_id)

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
