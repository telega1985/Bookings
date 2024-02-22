from app.database import Base
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Annotated


intpk = Annotated[int, mapped_column(primary_key=True, index=True)]


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[intpk]
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

    def __str__(self):
        return f"Отель {self.name}"
