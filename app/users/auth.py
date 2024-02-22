import uuid

from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from jose import jwt

from app.config import settings
from app.database import async_session_maker
from app.exceptions import IncorrectEmailOrPasswordException, TokenAbsentException, TokenExpiredException
from app.users.dao import UsersDAO, RefreshSessionDAO
from app.users.models import RefreshSession
from app.users.schemas import SToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def create_token(cls, user_id: int) -> SToken:
        access_token = cls.create_access_token(user_id)
        refresh_token = cls.create_refresh_token()
        refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        async with async_session_maker() as session:
            await RefreshSessionDAO.add(
                session,
                user_id=user_id,
                refresh_token=refresh_token,
                expires_in=refresh_token_expires.total_seconds()
            )
            await session.commit()

        return SToken(access_token=access_token, refresh_token=refresh_token)

    @classmethod
    def create_access_token(cls, user_id: int) -> str:
        to_encode = {
            "sub": str(user_id),
            "exp": datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

        return encoded_jwt

    @classmethod
    def create_refresh_token(cls) -> str:
        return uuid.uuid4()

    @classmethod
    async def authenticate_user(cls, email: str, password: str):
        async with async_session_maker() as session:
            db_user = await UsersDAO.find_one_or_none(session, email=email)

        if not (db_user and cls.verify_password(password, db_user.hashed_password)):
            raise IncorrectEmailOrPasswordException

        return db_user

    @classmethod
    async def logout(cls, token: uuid.UUID) -> None:
        async with async_session_maker() as session:
            refresh_session = await RefreshSessionDAO.find_one_or_none(session, refresh_token=token)

            if refresh_session:
                await RefreshSessionDAO.delete(session, id=refresh_session.id)

            await session.commit()

    @classmethod
    async def refresh_token(cls, token: uuid.UUID) -> SToken:
        async with async_session_maker() as session:
            refresh_session = await RefreshSessionDAO.find_one_or_none(session, refresh_token=token)

            if not refresh_session:
                raise TokenAbsentException
            if datetime.now(UTC) >= refresh_session.created_at + timedelta(seconds=refresh_session.expires_in):
                await RefreshSessionDAO.delete(session, id=refresh_session.id)
                raise TokenExpiredException

            user = await UsersDAO.find_one_or_none(session, id=refresh_session.user_id)

            if not user:
                raise TokenAbsentException

            access_token = cls.create_access_token(user.id)
            refresh_token = cls.create_refresh_token()
            refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

            await RefreshSessionDAO.update(
                session,
                RefreshSession.id == refresh_session.id,
                refresh_token=refresh_token,
                expires_in=refresh_token_expires.total_seconds()
            )
            await session.commit()

        return SToken(access_token=access_token, refresh_token=refresh_token)

