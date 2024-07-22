import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StoreCreation(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=255)
    logo_url: str = Field(max_length=255)


class StoreItemCreation(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=255)
    logo_url: str = Field(max_length=255)
    balance: int = Field(default=0)
    price_penny: int = Field(default=0)
    category: str = Field(max_length=100)


class StoreItem(StoreItemCreation):
    id: str


class Store(StoreCreation):
    id: str
    items: Optional[list[StoreItem]]


class PurchaseItem(BaseModel):
    item_id: str
    count: str


class Purchase(BaseModel):
    id: str
    store_id: str
    user_id: str
    items_ids: list[str]
    date: datetime.datetime


class Task(BaseModel):
    id: str
    purchase: Purchase
    store_id: str
    user_id: str
    is_ready: bool
    date: datetime.datetime
