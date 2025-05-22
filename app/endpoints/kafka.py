import logging
from typing import Optional

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError

from app.config import KafkaConfig
from app.cores.health_checker import HealthChecker

_logger = logging.getLogger(__name__)


class KafkaClient(HealthChecker):
    def __init__(self, config: KafkaConfig):
        self.name = "Kafka"
        self.bootstrap_servers = config.bootstrap_servers
        self.producer: Optional[AIOKafkaProducer] = None
        self.consumer: Optional[AIOKafkaConsumer] = None

    async def connect(self):
        """Initialize Kafka producer and consumer connections"""
        try:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: str(v).encode('utf-8')
            )
            await self.producer.start()
            
            # Initialize a basic consumer for health checks
            self.consumer = AIOKafkaConsumer(
                bootstrap_servers=self.bootstrap_servers,
                group_id="health-check-group"
            )
            await self.consumer.start()
        except Exception as exc:
            _logger.exception(f"Failed to connect to Kafka: {exc}")
            raise

    async def close(self):
        """Close Kafka connections"""
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()

    async def send_message(self, topic: str, value: str, key: Optional[str] = None):
        """Send a message to a Kafka topic"""
        if not self.producer:
            raise Exception("Kafka producer is not initialized")
        try:
            await self.producer.send_and_wait(
                topic=topic,
                value=value,
                key=key.encode('utf-8') if key else None
            )
        except KafkaError as exc:
            _logger.exception(f"Failed to send message to Kafka: {exc}")
            raise

    async def check_health(self):
        """Check if Kafka is healthy by attempting to list topics"""
        try:
            if not self.consumer:
                return False
            # Try to list topics as a health check
            await self.consumer.topics()
            return True
        except Exception as exc:
            _logger.exception(f"Exception in checking Kafka: {exc}")
            return False 