import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped

from model.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = Column(
        String(60),
        unique=True
    )
    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC)
    )
