from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional


class SBookingCreate(BaseModel):
    room_id: int
    date_from: date
    date_to: date


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


class SUserWithBookings(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str


class SBookingsWithUser(SBookingCreate):
    id: int
    user_id: int
    price: int
    total_cost: int
    total_days: int
    user: SUserWithBookings
