from pydantic import BaseModel, Field

from auth.engineer_privileges import EngineerPrivileges


class UserCreation(BaseModel):
    name: str = Field(max_length=255)
    face: str | None = Field(max_length=10_485_760, default=None)


class EngineerBase(BaseModel):
    login: str = Field(max_length=255)


class EngineerCreation(EngineerBase):
    password: str = Field(max_length=255)


class Engineer(EngineerBase):
    id: str


class EngineerPrivilegesUpdate(BaseModel):
    id: str
    privileges: list[EngineerPrivileges]


class UserFaceUpdate(BaseModel):
    face: str = Field(max_length=10_485_760)


class AuthCardCreation(BaseModel):
    key: str | None = Field(max_length=256, default=None)
