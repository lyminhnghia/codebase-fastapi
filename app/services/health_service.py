import logging
from typing import List

from app.cores.health_checker import HealthChecker

logger = logging.getLogger(__name__)


class HealthService:
    def __init__(self, services: List[HealthChecker]):
        self.services = services

    async def run_health_check(self):
        status = {}
        is_healthy = True
        for service in self.services:
            health_status = await service.check_health()
            status[service.name] = health_status
            if not health_status:
                is_healthy = False
        return status, is_healthy
