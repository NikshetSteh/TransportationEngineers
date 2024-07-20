from pydantic import BaseModel, Field


class UserCreation(BaseModel):
    name: str = Field(max_length=255)
    face: str = Field(max_length=10_485_760)
