import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import Mapped

from model.base import Base


class Attraction(Base):
    __tablename__ = "attractions"

    id: Mapped[str] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = Column(
        String(256)
    )
    description: Mapped[str] = Column(
        String(1024)
    )
    logo_url: Mapped[str] = Column(
        String(256)
    )
    destination_id: Mapped[str] = Column(
        String(256)
    )

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC)
    )


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[str] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = Column(
        String(256)
    )
    description: Mapped[str] = Column(
        String(1024)
    )
    logo_url: Mapped[str] = Column(
        String(256)
    )
    destination_id: Mapped[str] = Column(
        String(256)
    )

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC)
    )
