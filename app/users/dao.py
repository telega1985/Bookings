from app.users.models import Users, RefreshSession
from app.dao.base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users


class RefreshSessionDAO(BaseDAO):
    model = RefreshSession
