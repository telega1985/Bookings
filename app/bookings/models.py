from datetime import datetime

from app.database import Base
from sqlalchemy import Computed, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.hotels.models import intpk
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[intpk]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[datetime] = mapped_column(Date)
    date_to: Mapped[datetime] = mapped_column(Date)
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))

    user: Mapped["Users"] = relationship(back_populates="bookings")
    room: Mapped["Rooms"] = relationship(back_populates="bookings")

    def __str__(self):
        return f"Бронирование #{self.id}"
