import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, Enum, String
from sqlalchemy.orm import Mapped, relationship

from model.base import Base
from store.store_types import StoreType


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
    store_type: Mapped[StoreType] = Column(
        Enum(StoreType, name="store_type_enum", create_type=False)
    )

    # noinspection PyUnresolvedReferences
    items: Mapped[list["StoreItem"]] = relationship(back_populates="store")

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC)
    )
