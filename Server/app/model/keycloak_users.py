from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from model.base import Base


class KeycloakUser(Base):
    __tablename__ = "keycloak_users"

    k_id: Mapped[str] = Column(
        UUID,
        name="id",
        primary_key=True,
    )
    user_id = Column(UUID, ForeignKey("users.id"))
    user = relationship("User")
