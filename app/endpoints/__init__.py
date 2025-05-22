from app.config import Config, config
from app.endpoints.postgres import PostgresDB
from app.endpoints.redis import RedisClient


class EndpointManager:
    """
    Remote endpoint manager. Manage connect and close connection. With atributes : PostgresQL, Redis, etc.
    """

    def __init__(self, config: Config):
        self.config = config
        self.postgres = PostgresDB(config.postgres)
        self.redis = RedisClient(config.redis)

    async def connect(self):
        """
        Function that handles startup and shutdown events.
        To understand more, read https://fastapi.tiangolo.com/advanced/events/
        """
        await self.redis.connect()

    async def disconnect(self):
        """to release resources"""
        await self.postgres.session_manager.close()
        self.redis.close()


# Global endpoint manager with load config
endpoint = EndpointManager(config=config)
