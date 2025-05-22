class HealthChecker:
    def __init__(self, name: str) -> None:
        self.name = name

    async def check_health(self) -> bool:
        raise NotImplementedError
