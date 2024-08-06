import uuid

from sqlalchemy import UUID, Column, Integer
from sqlalchemy.orm import Mapped

from model.base import Base


class TrainStore(Base):
    __tablename__ = "train_stores"

    id: Mapped[str] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )
    store_id: Mapped[str] = Column(
        UUID,
        nullable=False
    )
    train_number: Mapped[int] = Column(
        Integer,
        nullable=False
    )
