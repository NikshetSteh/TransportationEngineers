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
