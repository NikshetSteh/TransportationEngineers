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
    face: str | None = Field(max_length=10_485_760)
    code: str | None


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


class DestinationDeterminationRequest(BaseModel):
    user_id: str = Field(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
    train_number: int
    start_date: datetime.datetime


class Destination(BaseModel):
    id: str
