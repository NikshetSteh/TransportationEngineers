from pydantic_settings import BaseSettings
from functools import lru_cache


class Config(BaseSettings):
    client_id: str = "ai_site"
    client_secret: str = "7mbHVQGTLUKSNXrNYowg26SMCKv1YeLe"

    auth_redirect_uri: str = "http://localhost:8090/realms/ai_site/protocol/openid-connect/auth"
    auth_token_uri: str = "http://localhost:8090/realms/ai_site/protocol/openid-connect/token"
    user_info_uri: str = "http://localhost:8090/realms/ai_site/protocol/openid-connect/userinfo"


@lru_cache
def get_config() -> Config:
    return Config()
