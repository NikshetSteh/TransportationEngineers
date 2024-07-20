from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    CHROMA_DB_HOST: str = "localhost"
    CHROMA_DB_PORT: int = 8010

    FACE_MODEL: str = "buffalo_l"
    FACE_MODEL_PROVIDER: str = "CPUExecutionProvider"
    FACE_MODEL_CTX_ID: int = 0
    FACE_MODEL_DET_SIZE: int = 256

    THRESHOLD: int = 400

    DB_URI: str = "postgresql+asyncpg://postgres:root@localhost:5432/TransportEngineers"

    SHOW_DB_ECHO: bool = False


@lru_cache()
def get_config() -> Config:
    return Config()


