from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        await session.execute(query)

    @classmethod
    async def update(cls, session: AsyncSession, *where, **data):
        query = update(cls.model).where(*where).values(**data).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()

    @classmethod
    async def add_bulk(cls, session: AsyncSession, *data):
        try:
            query = insert(cls.model).values(*data).returning(cls.model.id)
            result = await session.execute(query)
            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            msg = ""
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc"
            elif isinstance(e, Exception):
                msg = "Unknown Exc"

            msg += ": Cannot bulk insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
