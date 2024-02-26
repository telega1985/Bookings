from celery import Celery
from celery.schedules import crontab

from app.config import settings


celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled"
    ]
)

celery.conf.beat_schedule = {
    "email.booking_reminder_1day": {
        "task": "email.booking_reminder_1day",
        "schedule": crontab(minute="45", hour="10") # Каждое утро в 9:00
    },
    "email.booking_reminder_3days": {
        "task": "email.booking_reminder_3days",
        "schedule": crontab(minute="25", hour="18") # Каждое утро в 9:00
    },
    # "luboe-nazvanie": {
    #     "task": "periodic_task",
    #     "schedule": 10, # секунды
    #     # "schedule": crontab(minute="30", hour="15") # Если нужна сложная периодичность
    # }
}
