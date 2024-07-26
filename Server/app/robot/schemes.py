import datetime

from pydantic import BaseModel, Field


class IdentificationRequest(BaseModel):
    image: str = Field(max_length=10_485_760)


class Robot(BaseModel):
    id: str
    robot_model_id: str = Field(max_length=60)
    robot_model_name: str = Field(max_length=60)


class TicketValidationRequest(BaseModel):
    station_id: str = Field(max_length=60)
    train_number: int
    wagon_number: int
    date: datetime.datetime
    face: str = Field(max_length=10_485_760)


class Attraction(BaseModel):
    id: str
    name: str
    description: str
    logo_url: str


class Hotel(BaseModel):
    id: str
    name: str
    description: str
    logo_url: str


class EngineerRobotAccessRequest(BaseModel):
    key: str = Field(max_length=256)
