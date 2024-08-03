from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    KEY_PATH: str = "private"
    LOGIN_FILE_PATH: str = "private/login_data"

    BASE_API_URL: str = "http://localhost:8080/base_api/v1"
    STORE_API_URL: str = "http://localhost:8080/store_api/v1"
<<<<<<< HEAD
=======

    RESOURCE_URL: str = "http://localhost:8080"
>>>>>>> dev

    ROBOT_MODEL_ID: str = "TestRobotID1"
    ROBOT_MODEL_NAME: str = "TestRobot:0.1.0:001"


@lru_cache()
def get_config() -> Config:
    return Config()
