from pydantic import BaseModel, Field


class WebhookRequest(BaseModel):
    type: str
    realmId: str
    id: str | None = None
    time: int | None = None
    clientId: str | None = None
    userId: str | None = None
    ipAddress: str | None = None
    error: str | None = None
    details: dict | None = None
    resourcePath: str | None = None
    representation: str | None = None


class Face(BaseModel):
    face: str | None = Field(max_length=int(1.25 * 8 * 1024 * 1024), default=None)
