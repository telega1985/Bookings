from fastapi import APIRouter, Query
from datetime import date, datetime, timedelta

from fastapi_cache.decorator import cache

from app.hotels.schemas import SHotelInfo, SHotel
from app.hotels.service import HotelService
from typing import Optional

router_hotels = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router_hotels.get("/{location}")
# @cache(expire=30)
async def get_hotels_by_location(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}")
) -> list[SHotelInfo]:
    return await HotelService.service_get_hotels_by_location(location, date_from, date_to)


@router_hotels.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SHotel]:
    return await HotelService.service_get_hotel_by_id(hotel_id)


@router_hotels.get("")
async def get_all_hotels() -> list[SHotel]:
    return await HotelService.service_get_all_hotels()
