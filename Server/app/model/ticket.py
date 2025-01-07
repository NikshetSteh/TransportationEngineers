import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, relationship

from model.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = Column(UUID, ForeignKey("users.id"))
    user = relationship("User")

    train_number: Mapped[int] = Column(
        Integer
    )

    wagon_number: Mapped[int] = Column(
        Integer
    )

    place_number: Mapped[int] = Column(
        Integer
    )

    date: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True)
    )

    station_id: Mapped[str] = Column(
        String(60)
    )

    code: Mapped[str] = Column(
        String(128)
    )

    destination_id: Mapped[str] = Column(
        String(60)
    )
    start_date: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True)
    )

    used: Mapped[bool] = Column(
        Boolean,
        default=False
    )
