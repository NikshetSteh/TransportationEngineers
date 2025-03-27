from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    CLIENT_ID: str = "ai_site"
    CLIENT_SECRET: str = "7mbHVQGTLUKSNXrNYowg26SMCKv1YeLe"

    AUTH_REDIRECT_URI: str = "http://localhost/keycloak/realms/ai_site/protocol/openid-connect/auth"
    AUTH_TOKEN_URI: str = "http://localhost/keycloak/realms/ai_site/protocol/openid-connect/token"
    USER_INFO_URI: str = "http://localhost/keycloak/realms/ai_site/protocol/openid-connect/userinfo"

    ROBOT_API_URI: str = "http://localhost/base_api/v1"

    API_URI: str = "http://nginx"

    FRONTEND_URL: str | None = None

    MAX_IMAGE_SIZE: int = int(1.25 * 8 * 1024 * 1024)


@lru_cache
def get_config() -> Config:
    return Config()
