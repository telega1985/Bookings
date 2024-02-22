import asyncio
from datetime import datetime
import json

import pytest

from app.bookings.models import Bookings
from app.database import Base, async_session_maker, engine
from app.config import settings
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app as fastapi_app

from sqlalchemy import insert

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for model, values in [
            (Hotels, hotels),
            (Rooms, rooms),
            (Users, users),
            (Bookings, bookings)
        ]:
            query = insert(model).values(values)

            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    """
    Асинхронный клиент для тестирования эндпоинтов
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    """
    Асинхронный аутентифицированный клиент для тестирования эндпоинтов
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "telega.85@gmail.com",
            "password": "telega"
        })

        assert ac.cookies["access_token"]
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
