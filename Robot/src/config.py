from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    KEY_PATH: str = "private"


@lru_cache()
def get_config() -> Config:
    return Config()