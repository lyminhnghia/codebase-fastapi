import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.endpoints.redis import RedisClient
from app.config import RedisConfig


@pytest.fixture
def redis_config():
    return RedisConfig(uri="redis://localhost:6379")


@pytest.fixture
def redis_client(redis_config):
    return RedisClient(redis_config)


class TestRedisClient:
    @pytest.mark.asyncio
    async def test_connect(self, redis_client):
        with patch("aioredis.create_redis_pool") as mock_create_pool:
            mock_pool = AsyncMock()
            mock_create_pool.return_value = mock_pool

            await redis_client.connect()
            assert redis_client.redis == mock_pool
            mock_create_pool.assert_called_once_with(redis_client.redis_uri)

    def test_close_not_initialized(self, redis_client):
        with pytest.raises(Exception) as exc_info:
            redis_client.close()
        assert str(exc_info.value) == "RedisClient is not initialized"

    def test_close_success(self, redis_client):
        mock_redis = MagicMock()
        redis_client.redis = mock_redis
        redis_client.close()
        mock_redis.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_value(self, redis_client):
        mock_redis = AsyncMock()
        redis_client.redis = mock_redis

        await redis_client.set_value("test_key", "test_value", 3600)
        mock_redis.set.assert_called_once_with("test_key", "test_value", expire=3600)

    @pytest.mark.asyncio
    async def test_get_value(self, redis_client):
        mock_redis = AsyncMock()
        mock_redis.get.return_value = "test_value"
        redis_client.redis = mock_redis

        result = await redis_client.get_value("test_key")
        assert result == "test_value"
        mock_redis.get.assert_called_once_with("test_key")

    @pytest.mark.asyncio
    async def test_check_health_success(self, redis_client):
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        redis_client.redis = mock_redis

        result = await redis_client.check_health()
        assert result is True
        mock_redis.ping.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_health_failure(self, redis_client):
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock(side_effect=Exception("Connection error"))
        redis_client.redis = mock_redis

        result = await redis_client.check_health()
        assert result is False
