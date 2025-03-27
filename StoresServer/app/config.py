from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URI: str = (
        "postgresql+asyncpg://postgres:root@localhost:5432/TransportEngineersStores"
    )
    DB_URI_ALEMBIC: str = (
        "postgresql+psycopg2://postgres:root@localhost:5432/TransportEngineersStores"
    )
    SHOW_DB_ECHO: bool = True

    REDIS_URI: str = "redis://default:SuperPass@localhost:6379"
    AUTH_SESSION_TIMEOUT: int = 3600


@lru_cache()
def get_config() -> Config:
    return Config()
