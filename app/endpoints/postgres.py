import logging

from sqlalchemy import text

from app.config import PostgresConfig
from app.cores.database import DatabaseSessionManager
from app.cores.health_checker import HealthChecker

_logger = logging.getLogger(__name__)


class PostgresDB(HealthChecker):
    def __init__(self, config: PostgresConfig):
        self.name = "PostgresDB"
        self.session_manager = DatabaseSessionManager(
            self.async_uri(config.uri),
            {
                "echo": config.echo,
                "pool_size": config.pool_size,
                "max_overflow": config.max_overflow,
            },
        )

    def sync_uri(self, uri: str) -> str:
        splitted = uri.split("://")
        return "postgresql+psycopg2://" + splitted[1]

    def async_uri(self, uri: str) -> str:
        splitted = uri.split("://")
        return "postgresql+asyncpg://" + splitted[1]

    async def db_session(self):
        async with self.session_manager.session() as session:
            yield session

    async def check_health(self):
        try:
            async with self.session_manager.session() as session:
                await session.execute(text("SELECT 1"))
                return True
        except Exception as exc:
            _logger.exception(f"Exception in checking PostgreSQL: {exc}")
            return False
