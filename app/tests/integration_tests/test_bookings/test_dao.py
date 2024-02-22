import pytest

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookingCreate
from app.bookings.service import BookingService
from datetime import datetime

from app.users.dao import UsersDAO


# @pytest.mark.parametrize("user_id,room_id,date_from,date_to", [
#     (2, 2, datetime.strptime("2023-07-10", "%Y-%m-%d"), datetime.strptime("2023-07-24", "%Y-%m-%d"))
# ])
# async def test_add_and_get_booking(user_id, room_id, date_from, date_to, session):
#     user = await UsersDAO.find_one_or_none(session, id=user_id)
#     booking = SBookingCreate(room_id=room_id, date_from=date_from, date_to=date_to)
#     new_booking = await BookingService.service_add_booking_db(user, booking)
#
#     assert new_booking.user_id == user.id
#     assert new_booking.room_id == booking.room_id
#
#     new_booking = await BookingDAO.find_one_or_none(session, id=new_booking.id)
#
#     assert new_booking is not None


@pytest.mark.parametrize("user_id,room_id", [
    (1, 1),
    (2, 1),
    (1, 4)
])
async def test_booking_crud(user_id, room_id, session):
    # Добавление брони

    user = await UsersDAO.find_one_or_none(session, id=user_id)
    booking = SBookingCreate(
        room_id=room_id,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-20", "%Y-%m-%d")
    )
    new_booking = await BookingService.service_add_booking_db(user, booking)

    assert new_booking.user_id == user.id
    assert new_booking.room_id == booking.room_id

    # Проверка добавления брони

    new_booking = await BookingDAO.find_one_or_none(session, id=new_booking.id)

    assert new_booking is not None

    # Удаление брони

    await BookingService.service_remove_bookings(new_booking.id, user.id)

    # Проверка удаления брони

    deleted_booking = await BookingDAO.find_one_or_none(session, id=new_booking.id)

    assert deleted_booking is None
