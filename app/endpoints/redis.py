import logging

import aioredis

from app.config import RedisConfig
from app.cores.health_checker import HealthChecker

_logger = logging.getLogger(__name__)


class RedisClient(HealthChecker):
    def __init__(self, config: RedisConfig):
        self.name = "Redis"
        self.redis_uri = config.uri
        self.redis: aioredis.Redis = None

    async def connect(self):
        self.redis = await aioredis.create_redis_pool(self.redis_uri)

    def close(self):
        if self.redis is None:
            raise Exception("RedisClient is not initialized")
        self.redis.close()

    async def set_value(self, key: str, value: str, expire: int = 0):
        await self.redis.set(key, value, expire=expire)

    async def get_value(self, key: str):
        value = await self.redis.get(key)
        return value

    async def check_health(self):
        try:
            await self.redis.ping()
            return True
        except Exception as exc:
            _logger.exception(f"Exception in checking Redis: {exc}")
            return False
