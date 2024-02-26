from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.bookings.models import Bookings
from app.bookings.schemas import SBookingCreate
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all_with_images(cls, session: AsyncSession, user_id: int):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.room))
            .where(cls.model.user_id == user_id)
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_need_to_remind(cls, session: AsyncSession, days: int):
        """
        Список броней и пользователей, которым необходимо направить напоминание за days дней
        """
        query = (
            select(cls.model)
            .options(selectinload(cls.model.user))
            .where(date.today() == cls.model.date_from - timedelta(days=days))
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_rooms_booked(cls, session: AsyncSession, booking: SBookingCreate):
        """
        WITH booked_rooms AS (
            SELECT * FROM public.bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id)
        FROM rooms
        LEFT JOIN booked_rooms
        ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        booked_rooms = (
            select(cls.model)
            .where(
                and_(
                    cls.model.room_id == booking.room_id,
                    or_(
                        and_(
                            cls.model.date_from >= booking.date_from,
                            cls.model.date_from <= booking.date_to,
                        ),
                        and_(
                            cls.model.date_from <= booking.date_from,
                            cls.model.date_to > booking.date_from,
                        ),
                    ),
                )
            )
            .cte("booked_rooms")
        )

        get_rooms_left = (
            select(Rooms.quantity - func.count(booked_rooms.c.room_id))
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(Rooms.id == booking.room_id)
            .group_by(Rooms.quantity, booked_rooms.c.room_id)
        )

        rooms_left = await session.execute(get_rooms_left)
        rooms_left: int = rooms_left.scalar()

        get_price = select(Rooms.price).filter_by(id=booking.room_id)
        price = await session.execute(get_price)
        price: int = price.scalar()

        return rooms_left, price
