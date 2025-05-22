import os

from fastapi import APIRouter

from app.config import config

from .health_route import heath_router

build_module = os.getenv("BUILD_MODULE", "internal").lower()
router = APIRouter()
public_router = APIRouter()

public_router.include_router(heath_router, tags=["health"])
router.include_router(public_router, prefix=config.metadata.prefix)
