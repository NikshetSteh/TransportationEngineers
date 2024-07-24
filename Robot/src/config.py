from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    KEY_PATH: str = "private"
    LOGIN_FILE_PATH: str = "private/login_data"

    BASE_URL: str = "http://localhost:8000"

    ROBOT_MODEL_ID: str = "TestRobotID1"
    ROBOT_MODEL_NAME: str = "TestRobot:0.1.0:001"


@lru_cache()
def get_config() -> Config:
    return Config()
