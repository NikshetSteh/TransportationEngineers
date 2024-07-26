import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from model.base import Base
from model.engineer import Engineer


class AuthCard(Base):
    __tablename__ = "auth_cards"

    id: Mapped[str] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )

    engineer_id = Column(UUID, ForeignKey("engineers.id"))
    engineer = relationship(Engineer)

    key: Mapped[str] = Column(
        String(256),
        unique=True
    )

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC)
    )
