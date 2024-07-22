from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URI: str = "postgresql+asyncpg://postgres:root@localhost:5432/TransportEngineersStores"
    SHOW_DB_ECHO: bool = True


@lru_cache()
def get_config() -> Config:
    return Config()
