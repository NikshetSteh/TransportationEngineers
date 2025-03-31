from typing import Optional

from pydantic import BaseModel, Field
from store_api.store_types import StoreType


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
    name: str = Field(max_length=50)
    description: str = Field(max_length=255)
    logo_url: str = Field(max_length=255)
    store_type: StoreType
    items: Optional[list[StoreItem]]
