import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import Mapped, relationship

from model.base import Base


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = Column(
        String(100),
    )
    description: Mapped[str] = Column(
        String(255),
    )
    logo_url: Mapped[str] = Column(
        String(255),
    )

    # noinspection PyUnresolvedReferences
    items: Mapped[list["StoreItem"]] = relationship(back_populates="store")

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC)
    )
