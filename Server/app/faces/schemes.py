from pydantic import BaseModel, Field


class IdentificationRequest(BaseModel):
    image: str = Field(max_length=10_485_760)


class IdentificationResponse(BaseModel):
    user_id: str
    user_name: str
