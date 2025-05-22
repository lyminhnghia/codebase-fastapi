from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import config


def add_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.origin.allowed,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
