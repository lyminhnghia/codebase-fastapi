import pytest
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from app.cores.request_id import add_request_id


@pytest.mark.asyncio
async def test_add_request_id():
    app = FastAPI()
    add_request_id(app)

    # Check if CorrelationIdMiddleware was added with correct config
    for middleware in app.user_middleware:
        if middleware.cls is CorrelationIdMiddleware:
            assert middleware.options["header_name"] == "X-Request-ID"
            break
    else:
        pytest.fail("CorrelationIdMiddleware not found in user_middleware")
