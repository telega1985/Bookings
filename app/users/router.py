from fastapi import APIRouter, status, Response, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.config import settings
from app.exceptions import IncorrectEmailOrPasswordException
from app.users.auth import AuthService
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.service import UserService
from app.users.schemas import SUserCreate, SUserInfo, SToken

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@router_auth.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: SUserCreate) -> SUserInfo:
    create_user = await UserService.service_create_new_user(user)
    return create_user


async def json_oauth2_password_request_form(user: SUserCreate):
    return OAuth2PasswordRequestForm(username=user.email, password=user.password)


@router_auth.post("/login")
async def login_user(
        response: Response, credentials: OAuth2PasswordRequestForm = Depends(json_oauth2_password_request_form)
) -> SToken:
    user = await AuthService.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    token = await AuthService.create_token(user.id)

    response.set_cookie(
        "access_token",
        token.access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True
    )
    response.set_cookie(
        "refresh_token",
        token.refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
        httponly=True
    )

    return token


@router_auth.post("/logout")
async def logout_user(response: Response, request: Request, user: Users = Depends(get_current_user)):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    await AuthService.logout(request.cookies.get("refresh_token"))

    return {"authenticated": False}


@router_auth.post("/refresh")
async def refresh_token_user(request: Request, response: Response) -> SToken:
    new_token = await AuthService.refresh_token(request.cookies.get("refresh_token"))

    response.set_cookie(
        "access_token",
        new_token.access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True
    )
    response.set_cookie(
        "refresh_token",
        new_token.refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 30 * 24 * 60,
        httponly=True
    )
    return new_token


@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)) -> SUserInfo:
    return current_user
