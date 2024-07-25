from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    FACE_API: str = "http://127.0.0.1:8030/face_api/v1"
    STORE_API: str = "http://172.23.116.239:80/store_api/v1"

    DB_URI: str = "postgresql+asyncpg://postgres:root@localhost:5432/TransportEngineers"
    DB_URI_ALEMBIC: str = "postgresql+psycopg2://postgres:root@localhost:5432/TransportEngineers"

    SHOW_DB_ECHO: bool = False

    REDIS_URI: str = "redis://default:SuperPass@localhost:6379"

    SYMBOLS_POOL: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"
    AUTH_CODE_LENGTH: int = 100
    AUTH_REQUEST_TIMEOUT: int = 30
    AUTH_SESSION_TIMEOUT: int = 3600


@lru_cache()
def get_config() -> Config:
    return Config()


