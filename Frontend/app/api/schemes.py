from pydantic import BaseModel


class Profile(BaseModel):
    username: str
