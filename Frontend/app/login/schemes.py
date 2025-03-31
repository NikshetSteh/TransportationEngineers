from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expire_in: int
    refresh_expire_in: int
