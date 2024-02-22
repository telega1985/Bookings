from datetime import date

from app.database import async_session_maker
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomInfo


class RoomService:
    @classmethod
    async def service_get_rooms_by_time(cls, hotel_id: int, date_from: date, date_to: date) -> list[SRoomInfo]:
        async with async_session_maker() as session:
            return await RoomDAO.find_all_rooms(session, hotel_id, date_from, date_to)
