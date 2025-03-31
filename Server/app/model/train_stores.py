import datetime
import uuid

from model.base import Base
from sqlalchemy import UUID, Column, DateTime, Integer
from sqlalchemy.orm import Mapped


class TrainStore(Base):
    __tablename__ = "train_stores"

    id: Mapped[str] = Column(UUID, name="id", primary_key=True, default=uuid.uuid4)
    store_id: Mapped[str] = Column(UUID, nullable=False)
    train_number: Mapped[int] = Column(Integer, nullable=False)
    train_date: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), nullable=False
    )
