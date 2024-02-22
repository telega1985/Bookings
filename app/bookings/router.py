from fastapi import APIRouter, Depends, status

from app.bookings.schemas import SBookingCreate, SBookingBookedInfo, SBookingWithRoom
from app.bookings.service import BookingService
from app.users.dependencies import get_current_user
from app.users.models import Users

router_booking = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router_booking.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingWithRoom]:
    return await BookingService.service_get_bookings(user.id)


@router_booking.post("", status_code=status.HTTP_201_CREATED)
async def add_booking(booking: SBookingCreate, user: Users = Depends(get_current_user)) -> SBookingBookedInfo:
    return await BookingService.service_add_booking_db(user, booking)


@router_booking.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingService.service_remove_bookings(booking_id, user.id)
