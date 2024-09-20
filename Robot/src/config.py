from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    KEY_PATH: str = "private"
    LOGIN_FILE_PATH: str = "private/login_data"

    BASE_API_URL: str = "http://localhost:8080/base_api/v1"
    STORE_API_URL: str = "http://localhost:8080/store_api/v1"

    RESOURCE_URL: str = "http://localhost:8080"

    ROBOT_MODEL_ID: str = "TestRobotID1"
    ROBOT_MODEL_NAME: str = "TestRobot:0.1.0:001"

    # DEFAULT_STORE: str = "0ebdbfc3-0e2c-4ce2-ac69-a414437c0482"
    DEFAULT_STORE: str = "8041baff-c89f-4ce0-9cde-997629cf554c"


@lru_cache()
def get_config() -> Config:
    return Config()
