from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    KEY_PATH: str = "private"
    LOGIN_FILE_PATH: str = "private/login_data"


@lru_cache()
def get_config() -> Config:
    return Config()
