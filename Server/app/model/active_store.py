import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import Mapped

from model.base import Base


class ActiveStore(Base):
    __tablename__ = "active_stores"

    id: Mapped[int] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )

    public_key: Mapped[str] = Column(
        String(500)
    )

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC)
    )
