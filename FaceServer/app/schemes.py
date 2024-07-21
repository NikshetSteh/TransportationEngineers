from pydantic import BaseModel, Field


class NewFaceRequest(BaseModel):
    user_id: str
    image: str = Field(max_length=10_485_760)


class SearchFaceRequest(BaseModel):
    image: str = Field(max_length=10_485_760)


class EmptyResponse(BaseModel):
    status: str = Field(default="OK")


class User(BaseModel):
    user_id: str
