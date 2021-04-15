"""Redis-based cache for app data."""

from typing import Optional

from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis

from common.debug_tools import log_method
# from common.schemas import UserSchema, AccountSchema, \
#     CategorySchema, TemplateSchema, EventSchema
# from common.constants import ENTITY, ENTITY_SCHEMAS


class CacheService:
    """Redis-based cache for app data."""

    name = "cache_service"
    redis = Redis('redis')
    db_service = RpcProxy('db_service')

    # @rpc
    # @log_method
    # def get(self, entity_type, entity_id):
    #     """Get some stuff from cache or db."""
    #     schema = ENTITY_SCHEMAS[entity_type]()
    #     entity_raw = self.redis.hget(entity_type, entity_id)
    #     if entity_raw is None:
    #         entity_raw = getattr(
    #             self.db_service, f'get_{entity_type}'
    #         )(entity_id)
    #         if entity_raw is None:
    #             return None
    #         else:
    #             stuff = schema.load(entity_raw)
    #             self.redis.hset(entity_type, entity_id, schema.dumps(stuff))
    #     else:
    #         stuff = schema.loads(json_data=entity_raw)
    #     return schema.dump(stuff)

    @rpc
    @log_method
    def forget(self, entity_type, entity_id):
        """Remove stuff from cache."""
        self.redis.hdel(entity_type, entity_id)

    @rpc
    @log_method
    def clear(self):
        """Clear cache."""
        self.redis.flushdb()
