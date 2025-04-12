from pydantic import BaseModel, Field


def keycloak_id_strip(s: str) -> str:
    if s.startswith("f:"):
        return s.split(":")[2]

    return s


class ProvidedUserBase(BaseModel):
    username: str = ""
    full_name: str = ""
    email: str = ""


class ProvidedUser(ProvidedUserBase):
    id: str
    created_at: int


class ProvidedUserCreation(ProvidedUserBase):
    password: str


class ProvidedUserPatch(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None


class UserCredentials(BaseModel):
    user_id: str
    password: str


class CredentialsValidationResult(BaseModel):
    valid: bool


class UserQuery(BaseModel):
    start: int = 0
    limit: int = 100
    params: dict[str, str] = Field(default_factory=dict)
