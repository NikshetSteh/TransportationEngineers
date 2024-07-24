import datetime

from pydantic import BaseModel


class Ticket(BaseModel):
    id: str
    user_id: str
    train_number: int
    wagon_number: int
    place_number: int
    station_id: str
    date: datetime.datetime
