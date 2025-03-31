import datetime
import uuid

from model.base import Base
from sqlalchemy import UUID, Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped


class Engineer(Base):
    __tablename__ = "engineers"

    id: Mapped[int] = Column(UUID, name="id", primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = Column(String(60), unique=True)
    password: Mapped[str] = Column(String(60))
    privileges: Mapped[int] = Column(Integer, default=0)
    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC)
    )
