from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    KEY_PATH: str = "private"
    LOGIN_FILE_PATH: str = "private/login_data"

    BASE_API_URL: str = "http://localhost/base_api/v1"
    STORE_API_URL: str = "http://localhost/store_api/v1"

    RESOURCE_URL: str = "http://localhost"

    ROBOT_MODEL_ID: str = "TestRobotID1"
    ROBOT_MODEL_NAME: str = "TestRobot:0.1.0:001"

    DEFAULT_STORE: str = "07ed497d-da82-4992-9b67-14bc3fd3fa86"


@lru_cache()
def get_config() -> Config:
    return Config()
