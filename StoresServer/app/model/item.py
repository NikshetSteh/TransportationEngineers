import datetime
import uuid

from model.base import Base
from model.history import Purchase
from model.store import Store
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class StoreItem(Base):
    __tablename__ = "store_items"

    id: Mapped[int] = Column(UUID, name="id", primary_key=True, default=uuid.uuid4)

    store_id: Mapped[str] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    store: Mapped["Store"] = relationship(back_populates="items")

    name: Mapped[str] = Column(
        String(100),
    )
    description: Mapped[str] = Column(
        String(255),
    )
    logo_url: Mapped[str] = Column(
        String(255),
    )

    balance: Mapped[int] = Column(Integer)
    price_penny: Mapped[int] = Column(Integer)
    category: Mapped[str] = Column(String(100))

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True), default=datetime.datetime.now(datetime.UTC)
    )


class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id: Mapped[int] = Column(UUID, name="id", primary_key=True, default=uuid.uuid4)

    purchase_id: Mapped[str] = mapped_column(
        ForeignKey("purchases.id", ondelete="CASCADE")
    )
    purchase: Mapped["Purchase"] = relationship(back_populates="items")

    store_item_id: Mapped[str] = mapped_column(
        ForeignKey("store_items.id", ondelete="CASCADE")
    )
    store_item: Mapped["StoreItem"] = relationship()
    count: Mapped[int] = Column(Integer)
