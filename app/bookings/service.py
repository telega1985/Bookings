from app.bookings.schemas import SBookingCreate, SBookingBookedInfo, SBookingWithRoom
from app.database import async_session_maker
from app.bookings.dao import BookingDAO
from app.exceptions import RoomCannotBeBooked
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger
from app.tasks.tasks import send_booking_confirmation_email
from app.users.models import Users


class BookingService:
    @classmethod
    async def service_get_bookings(cls, user_id: int) -> list[SBookingWithRoom]:
        async with async_session_maker() as session:
            return await BookingDAO.find_all_with_images(session, user_id)

    @classmethod
    async def service_add_booking_db(cls, user: Users, booking: SBookingCreate) -> SBookingBookedInfo:
        try:
            async with async_session_maker() as session:
                rooms_left, price = await BookingDAO.get_rooms_booked(session, booking)

                if rooms_left > 0:
                    add_booking = await BookingDAO.add(
                        session,
                        user_id=user.id,
                        **booking.model_dump(),
                        price=price
                    )

                    await session.commit()

                    booking_dict = SBookingBookedInfo(
                        id=add_booking.id,
                        user_id=add_booking.user_id,
                        room_id=add_booking.room_id,
                        date_from=add_booking.date_from,
                        date_to=add_booking.date_to
                    )
                    booking_data_dict = booking_dict.model_dump()
                    send_booking_confirmation_email.delay(booking_data_dict, user.email)
                    return booking_dict
                else:
                    raise RoomCannotBeBooked
        except (SQLAlchemyError, Exception) as e:
            msg = ""
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"

            msg += ": Cannot add booking"
            extra = {
                "user_id": user.id,
                "room_id": booking.room_id,
                "date_from": booking.date_from,
                "date_to": booking.date_to
            }

            logger.error(msg, extra=extra, exc_info=True)

    @classmethod
    async def service_remove_bookings(cls, booking_id: int, user_id: int):
        async with async_session_maker() as session:
            await BookingDAO.delete(session, id=booking_id, user_id=user_id)
            await session.commit()
