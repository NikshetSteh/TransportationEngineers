import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, String
from sqlalchemy.orm import Mapped

from model.base import Base


class Robot(Base):
    __tablename__ = "robots"

    id: Mapped[str] = Column(
        UUID,
        name="id",
        primary_key=True,
        default=uuid.uuid4
    )

    robot_model_id: Mapped[str] = Column(
        String(60),
        unique=True
    )
    robot_model_name: Mapped[str] = Column(
        String(60)
    )

    public_key: Mapped[str] = Column(
        String(500)
    )

    created_at: Mapped[datetime.datetime] = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC)
    )
