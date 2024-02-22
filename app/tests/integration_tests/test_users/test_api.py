from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("kot@pes.com", "kotopes", 201),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "pesokot", 201),
    ("dsadsa", "pesokot", 422)
])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("telega.85@gmail.com", "telega", 200),
    ("test@test.com", "test", 200),
    ("wrong@person.com", "egor", 401)
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code
