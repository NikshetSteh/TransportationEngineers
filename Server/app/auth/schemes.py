from pydantic import BaseModel, Field


class NewLogin(BaseModel):
    login: str
    password: str

    public_key: str
    robot_model_id: str = Field(max_length=60)
    robot_model_name: str = Field(max_length=60)


class LoginCode(BaseModel):
    data: str
    request_id: str


class LoginRequest(BaseModel):
    id: str


class AuthResponse(BaseModel):
    token: str
