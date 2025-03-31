import datetime
import uuid

from model.base import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = Column(UUID, name="id", primary_key=True, default=uuid.uuid4)

    store_id: Mapped[str] = Column(UUID, ForeignKey("stores.id", ondelete="CASCADE"))
    store = relationship("Store")

    user_id: Mapped[str] = Column(UUID)

    # noinspection PyUnresolvedReferences
    items: Mapped[list["PurchaseItem"]] = relationship(
        back_populates="purchase", lazy="selectin"
    )

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC)
    )
