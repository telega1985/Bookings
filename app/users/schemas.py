import uuid
from pydantic import BaseModel, EmailStr


class SUserBase(BaseModel):
    email: EmailStr


class SUserCreate(SUserBase):
    password: str


class SUserInfo(SUserBase):
    id: int
    hashed_password: str


class SToken(BaseModel):
    access_token: str
    refresh_token: uuid.UUID
