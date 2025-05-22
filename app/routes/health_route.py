from fastapi import APIRouter, Response, status

from app.dto.response_dto import BaseResponseData
from app.endpoints import endpoint
from app.services.health_service import HealthService

heath_router = APIRouter()


@heath_router.get("/ping", status_code=200, response_model=BaseResponseData)
async def health_check(response: Response):
    health_service = HealthService(services=[endpoint.postgres, endpoint.redis])
    health_status, is_healthy = await health_service.run_health_check()
    if not is_healthy:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return BaseResponseData(message="Server is not working", data=health_status)
    return BaseResponseData(message="Server is working", data=health_status)
