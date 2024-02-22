import uuid
from datetime import datetime
from app.database import Base
from sqlalchemy import UUID, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.hotels.models import intpk


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[str]
    hashed_password: Mapped[str]

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")

    def __str__(self):
        return f"Пользователь {self.email}"


class RefreshSession(Base):
    __tablename__ = "refresh_session"

    id: Mapped[intpk]
    refresh_token: Mapped[uuid.UUID] = mapped_column(UUID, index=True)
    expires_in: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
