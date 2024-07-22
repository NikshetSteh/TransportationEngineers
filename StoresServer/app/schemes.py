from pydantic import BaseModel, Field


class EmptyResponse(BaseModel):
    status: str = Field(default="OK")
