from datetime import datetime, UTC

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import (
    TokenAbsentException,
    IncorrectTokenFormatException,
    TokenExpiredException,
    UserIsNotPresentException
)
from app.users.service import UserService


class GetTokenOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl: str):
        super().__init__(tokenUrl=tokenUrl)

    def __call__(self, request: Request) -> str:
        token = request.cookies.get("access_token")
        if not token:
            raise TokenAbsentException

        return token


oauth2_scheme = GetTokenOAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")

    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise TokenExpiredException

    user_id: str = payload.get("sub")

    if not user_id:
        raise UserIsNotPresentException

    current_user = await UserService.get_authorization_user(int(user_id))

    if not current_user:
        raise UserIsNotPresentException

    return current_user
