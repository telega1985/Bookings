import pytest

from app.users.dao import UsersDAO


@pytest.mark.parametrize("email,exists", [
    ("telega.85@gmail.com", True),
    ("test@test.com", True),
    ("fake@fake.com", False)
])
async def test_find_user_by_id(email, exists, session):
    user = await UsersDAO.find_one_or_none(session, email=email)

    if exists:
        assert user
        assert user.email == email
    else:
        assert not user
