from pydantic import BaseModel


class EmptyResponse(BaseModel):
    status: str = "OK"
