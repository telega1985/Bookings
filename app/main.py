import time
import sentry_sdk
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router_booking
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router_rooms
from app.hotels.router import router_hotels
from app.images.router import router_images
from app.importer.router import router_importer
from app.logger import logger
from app.pages.router import router_frontend
from app.users.router import router_auth, router_users

# Sentry

sentry_sdk.init(
    dsn="https://ad2122a2469f6d907679fae6161f74a8@o4505895820460032.ingest.sentry.io/4505895834877952",
    enable_tracing=True,
)

# Redis cache

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    # При выключении


app = FastAPI(
    title="Бронирование отелей",
    version="0.1.0",
    lifespan=lifespan
)


# Основные роутеры

app.include_router(router_booking)
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_hotels)

# Загрузка картинок

app.include_router(router_images)

# Frontend

app.include_router(router_frontend)

# Загрузка тестовых данных на сервер

app.include_router(router_importer)

# Версионирование API

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api/v{major}",
    lifespan=lifespan
)

# Prometheus

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"]
)

instrumentator.instrument(app).expose(app)

# Доступы для фронтенда для взаимодействия с нашим api

origins = [
    "http://localhost:8000",
    "http://localhost:7777"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type", "Set-Cookie",
        "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
        "Authorization"
    ]
)

# Админка

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)

# Путь к папке static (frontend)

app.mount("/static", StaticFiles(directory="app/static"), "static")

# Middleware для logger

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })

    return response
