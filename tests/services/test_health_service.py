import pytest

from app.cores.health_checker import HealthChecker
from app.services.health_service import HealthService


class MockHealthChecker(HealthChecker):
    def __init__(self, name: str, healthy: bool):
        super().__init__(name)
        self.healthy = healthy

    async def check_health(self) -> bool:
        return self.healthy


@pytest.mark.asyncio
async def test_run_health_check_all_healthy():
    # All services return True
    checker_a = MockHealthChecker("DBService", True)
    checker_b = MockHealthChecker("CacheService", True)

    service = HealthService([checker_a, checker_b])
    status, is_healthy = await service.run_health_check()

    assert status == {"DBService": True, "CacheService": True}
    assert is_healthy is True


@pytest.mark.asyncio
async def test_run_health_check_some_unhealthy():
    # One service returns False
    checker_a = MockHealthChecker("DBService", True)
    checker_b = MockHealthChecker("CacheService", False)

    service = HealthService([checker_a, checker_b])
    status, is_healthy = await service.run_health_check()

    assert status == {"DBService": True, "CacheService": False}
    assert is_healthy is False


@pytest.mark.asyncio
async def test_run_health_check_no_services():
    # Empty list of services
    service = HealthService([])
    status, is_healthy = await service.run_health_check()

    assert status == {}
    assert is_healthy is True
