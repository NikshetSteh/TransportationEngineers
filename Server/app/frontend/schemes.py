from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Station(Enum):
    MOSCOW = "MOSCOW"
    SPB = "SPB"


class TicketCreation(BaseModel):
    train_number: int = 1012
    wagon_number: int
    place_number: int
    station_id: Station
    destination_id: Station
    date: datetime


class PasswordChangeRequest(BaseModel):
    old_password: str = Field(max_length=256)
    new_password: str = Field(max_length=256)
