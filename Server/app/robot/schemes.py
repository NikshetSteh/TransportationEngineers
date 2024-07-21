from pydantic import BaseModel, Field


class IdentificationRequest(BaseModel):
    image: str = Field(max_length=10_485_760)


class Robot(BaseModel):
    id: str
    robot_model_id: str = Field(max_length=60)
    robot_model_name: str = Field(max_length=60)
