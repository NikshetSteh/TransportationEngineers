from pydantic import BaseModel


class Attraction(BaseModel):
    id: str
    name: str
    description: str
    logo_url: str


class Hotel(BaseModel):
    id: str
    name: str
    description: str
    logo_url: str
