import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, AfterValidator


def date_timezone_converter(date: datetime.datetime) -> datetime.datetime:
    return date.astimezone(datetime.timezone(datetime.timedelta(hours=3)))


class Station(Enum):
    MOSCOW = "MOSCOW"
    SPB = "SPB"


class TicketCreation(BaseModel):
    train_number: int = 1012
    wagon_number: int
    place_number: int
    station_id: Station
    destination_id: Station
    date: Annotated[datetime.datetime, AfterValidator(date_timezone_converter)]


class PasswordChangeRequest(BaseModel):
    old_password: str = Field(max_length=256)
    new_password: str = Field(max_length=256)
