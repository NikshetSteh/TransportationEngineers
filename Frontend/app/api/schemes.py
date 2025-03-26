from pydantic import BaseModel


class Profile(BaseModel):
    username: str


class EmptyResponse(BaseModel):
    status: str = "OK"
