from fastapi import Query
from datetime import date, datetime, timedelta

from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.rooms.service import RoomService
from app.hotels.router import router_hotels as router_rooms


@router_rooms.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
) -> list[SRoomInfo]:
    return await RoomService.service_get_rooms_by_time(hotel_id, date_from, date_to)
