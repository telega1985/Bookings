from datetime import date
from pydantic import BaseModel
from typing import Optional


class SBookingCreate(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SBookingBookedInfo(SBookingCreate):
    id: int
    user_id: int


class SRoomsForBooking(BaseModel):
    image_id: int
    name: str
    description: Optional[str]
    services: list[str]


class SBookingWithRoom(SBookingCreate):
    id: int
    user_id: int
    price: int
    total_cost: int
    total_days: int
    room: SRoomsForBooking
