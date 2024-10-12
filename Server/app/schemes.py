import datetime

from pydantic import BaseModel


class EmptyResponse(BaseModel):
    status: str = "OK"


class TrainData(BaseModel):
    train_number: int
    train_date: datetime.datetime
