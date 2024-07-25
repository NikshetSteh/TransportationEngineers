import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class StoreType(Enum):
    SHOP = "SHOP"
    RESTAURANT = "RESTAURANT"


class StoreItem(BaseModel):
    id: str
    name: str = Field(max_length=50)
    description: str = Field(max_length=255)
    logo_url: str = Field(max_length=255)
    balance: int = Field(default=0)
    price_penny: int = Field(default=0)
    category: str = Field(max_length=100)


class Store(BaseModel):
    id: str
    items: Optional[list[StoreItem]]
    name: str = Field(max_length=50)
    description: str = Field(max_length=255)
    logo_url: str = Field(max_length=255)
    store_type: StoreType


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
