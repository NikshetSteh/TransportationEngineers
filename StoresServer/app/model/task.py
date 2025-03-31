import datetime
import uuid

from model.base import Base
from model.history import Purchase
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, relationship


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = Column(UUID, name="id", primary_key=True, default=uuid.uuid4)

    store_id: Mapped[str] = Column(UUID, ForeignKey("stores.id", ondelete="CASCADE"))

    user_id: Mapped[str] = Column(UUID)

    purchase_id: Mapped[str] = Column(
        UUID, ForeignKey("purchases.id", ondelete="CASCADE")
    )
    purchase: Mapped["Purchase"] = relationship("Purchase")

    is_ready: Mapped[bool] = Column(Boolean)
    additional_data: Mapped[dict] = Column(JSON)

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC)
    )
