import datetime
import uuid

from model.base import Base
from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import Mapped


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = Column(
        UUID, name="id", primary_key=True, default=uuid.uuid4, nullable=False
    )
    name: Mapped[str] = Column(String(60), unique=True, nullable=False)
    email: Mapped[str] = Column(String(256), unique=True, nullable=False)
    username: Mapped[str] = Column(String(256), unique=True, nullable=False)
    password: Mapped[str] = Column(String(256), nullable=False)
    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC),
        nullable=False,
    )
