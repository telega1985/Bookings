from app.database import async_session_maker
from app.exceptions import UserNotFound, UserAlreadyExistsException
from app.users.auth import AuthService
from app.users.dao import UsersDAO
from app.users.schemas import SUserCreate, SUserInfo


class UserService:
    @classmethod
    async def get_authorization_user(cls, user_id: int):
        async with async_session_maker() as session:
            db_user = await UsersDAO.find_one_or_none(session, id=user_id)

        if not db_user:
            raise UserNotFound

        return db_user

    @classmethod
    async def service_create_new_user(cls, user: SUserCreate) -> SUserInfo:
        async with async_session_maker() as session:
            existing_user = await UsersDAO.find_one_or_none(session, email=user.email)
            if existing_user:
                raise UserAlreadyExistsException

            hashed_password = AuthService.get_password_hash(user.password)

            db_user = await UsersDAO.add(
                session,
                **user.model_dump(exclude={"password"}),
                hashed_password=hashed_password
            )
            await session.commit()

        return db_user
