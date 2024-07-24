import datetime
from typing import Optional

from pydantic import BaseModel, Field

from store.store_types import StoreType


class StoreCreation(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=255)
    logo_url: str = Field(max_length=255)
    store_type: StoreType


class StoreItemCreation(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=255)
    logo_url: str = Field(max_length=255)
    balance: int
    price_penny: int
    category: str = Field(max_length=100)


class StoreItem(StoreItemCreation):
    id: str


class Store(StoreCreation):
    id: str
    items: Optional[list[StoreItem]]


class PurchaseItem(BaseModel):
    item_id: str
    count: int


class PurchaseCreation(BaseModel):
    user_id: str
    items: list[PurchaseItem]
    is_default_ready: bool
    additional_data: dict = Field(default={})


class Purchase(BaseModel):
    id: str
    store_id: str
    user_id: str
    items: list[PurchaseItem]
    date: datetime.datetime


class Task(BaseModel):
    id: str
    purchase: Purchase
    store_id: str
    user_id: str
    is_ready: bool
    date: datetime.datetime
    additional_data: dict
