from typing import List, Optional

import tomli
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DebugConfig(BaseModel):
    log_level: int


class Origin(BaseSettings):
    allowed: List[str] = []


class MetadataConfig(BaseModel):
    prefix: str
    swagger: Optional[bool] = False


class PostgresConfig(BaseModel):
    uri: str
    max_overflow: int
    pool_size: int
    echo: bool


class RedisConfig(BaseModel):
    uri: str


class Config(BaseSettings):
    """
    Global config use for service with debug, origin
    """

    debug: DebugConfig
    origin: Origin
    metadata: MetadataConfig
    postgres: PostgresConfig
    redis: RedisConfig


# Load config from settings.toml
with open("config/settings.toml", "rb") as f:
    config_data = tomli.load(f)

try:
    with open("config/.secrets.toml", "rb") as f:
        secret_data = tomli.load(f)
    config_data.update(secret_data)
except FileNotFoundError:
    pass

config = Config(**config_data)
