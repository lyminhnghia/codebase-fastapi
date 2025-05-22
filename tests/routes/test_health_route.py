from unittest.mock import AsyncMock, patch


# Original test renamed and modified to expect successful response
async def test_check_health_success(client):
    with patch(
        "app.services.health_service.HealthService.run_health_check",
        new_callable=AsyncMock,
    ) as mock_health_check:
        # Mock successful health check
        mock_health_check.return_value = ({"PostgresDB": True, "Redis": True}, True)

        resp = client.get("/api/v1/ping")
        assert resp.status_code == 200
        assert resp.json() == {
            "error_code": 0,
            "message": "Server is working",
            "data": {"PostgresDB": True, "Redis": True},
        }


# Test for when services are unavailable
async def test_check_health_unavailable(client):
    with patch(
        "app.services.health_service.HealthService.run_health_check",
        new_callable=AsyncMock,
    ) as mock_health_check:
        # Mock unsuccessful health check
        mock_health_check.return_value = ({"PostgresDB": False, "Redis": False}, False)

        resp = client.get("/api/v1/ping")
        assert resp.status_code == 503
        assert resp.json() == {
            "error_code": 0,
            "message": "Server is not working",
            "data": {"PostgresDB": False, "Redis": False},
        }


# Test when only PostgresDB is down
async def test_check_health_postgres_down(client):
    with patch(
        "app.services.health_service.HealthService.run_health_check",
        new_callable=AsyncMock,
    ) as mock_health_check:
        mock_health_check.return_value = ({"PostgresDB": False, "Redis": True}, False)

        resp = client.get("/api/v1/ping")
        assert resp.status_code == 503
        assert resp.json() == {
            "error_code": 0,
            "message": "Server is not working",
            "data": {"PostgresDB": False, "Redis": True},
        }


# Test when only Redis is down
async def test_check_health_redis_down(client):
    with patch(
        "app.services.health_service.HealthService.run_health_check",
        new_callable=AsyncMock,
    ) as mock_health_check:
        mock_health_check.return_value = ({"PostgresDB": True, "Redis": False}, False)

        resp = client.get("/api/v1/ping")
        assert resp.status_code == 503
        assert resp.json() == {
            "error_code": 0,
            "message": "Server is not working",
            "data": {"PostgresDB": True, "Redis": False},
        }
