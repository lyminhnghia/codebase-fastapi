from app.config import Config, config
from app.endpoints.postgres import PostgresDB
from app.endpoints.redis import RedisClient
from app.endpoints.kafka import KafkaClient


class EndpointManager:
    """
    Remote endpoint manager. Manage connect and close connection. With atributes : PostgresQL, Redis, Kafka, etc.
    """

    def __init__(self, config: Config):
        self.config = config
        self.postgres = PostgresDB(config.postgres)
        self.redis = RedisClient(config.redis)
        self.kafka = KafkaClient(config.kafka)

    async def connect(self):
        """
        Function that handles startup and shutdown events.
        To understand more, read https://fastapi.tiangolo.com/advanced/events/
        """
        await self.redis.connect()
        await self.kafka.connect()

    async def disconnect(self):
        """to release resources"""
        await self.postgres.session_manager.close()
        self.redis.close()
        await self.kafka.close()


# Global endpoint manager with load config
endpoint = EndpointManager(config=config)
