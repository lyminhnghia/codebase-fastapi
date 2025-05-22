from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.config import config
from app.cores.cors import add_cors
from app.cores.exception_handlers import add_exception_handlers
from app.cores.limiters import add_limiters
from app.cores.request_id import add_request_id
from app.cores.response_time import add_response_time
from app.endpoints import endpoint
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await endpoint.connect()
        yield
    finally:
        await endpoint.disconnect()


def create_app():
    app = FastAPI(
        lifespan=lifespan,
        docs_url=f"{config.metadata.prefix if config.metadata.swagger else ''}/docs",
        redoc_url=f"{config.metadata.prefix if config.metadata.swagger else ''}/redoc",
        openapi_url=f"{config.metadata.prefix if config.metadata.swagger else ''}/openapi.json",
    )
    add_limiters(app)
    add_request_id(app)
    add_response_time(app)
    add_cors(app)
    add_exception_handlers(app)
    app.include_router(router)

    return app


# To run locally
if __name__ == "__main__":
    uvicorn.run(create_app, host="0.0.0.0", port=8000)
