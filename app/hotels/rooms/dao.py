from datetime import date

from app.bookings.models import Bookings
from app.dao.base import BaseDAO

from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all_rooms(cls, session: AsyncSession, hotel_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            GROUP BY room_id
        )
        SELECT *, (quantity - COALESCE(rooms_booked, 0)) AS rooms_left
        FROM rooms
        LEFT JOIN booked_rooms
        ON booked_rooms.room_id = rooms.id
        WHERE hotel_id = 1
        """
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from
                    )
                )
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        get_rooms = (
            select(
                cls.model.__table__.columns,
                (cls.model.price * (date_to - date_from).days).label("total_cost"),
                (cls.model.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label("rooms_left")
            )
            .join(booked_rooms, booked_rooms.c.room_id == cls.model.id, isouter=True)
            .where(cls.model.hotel_id == hotel_id)
        )

        rooms = await session.execute(get_rooms)
        return rooms.mappings().all()
