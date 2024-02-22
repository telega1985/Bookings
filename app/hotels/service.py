from datetime import date

from app.database import async_session_maker
from app.exceptions import DateFromCannotBeAfterDateTo, CannotBookHotelForLongPeriod
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotelInfo, SHotel
from typing import Optional


class HotelService:
    @classmethod
    async def service_get_hotels_by_location(cls, location: str, date_from: date, date_to: date) -> list[SHotelInfo]:
        if date_from > date_to:
            raise DateFromCannotBeAfterDateTo
        if (date_to - date_from).days > 31:
            raise CannotBookHotelForLongPeriod

        async with async_session_maker() as session:
            return await HotelDAO.find_all_hotels(session, location, date_from, date_to)

    @classmethod
    async def service_get_hotel_by_id(cls, hotel_id: int) -> Optional[SHotel]:
        async with async_session_maker() as session:
            return await HotelDAO.find_one_or_none(session, id=hotel_id)

    @classmethod
    async def service_get_all_hotels(cls) -> list[SHotel]:
        async with async_session_maker() as session:
            return await HotelDAO.get_list_hotels(session)
