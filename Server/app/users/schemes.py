from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str


class TicketCreation(BaseModel):
    user_id: str
    train_number: int
    wagon_number: int
    place_number: int
    station_id: str
    destination: str
    date: datetime
    start_date: datetime


class Ticket(TicketCreation):
    id: str
    code: str = ""
