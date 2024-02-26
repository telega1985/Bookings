import asyncio

from app.tasks.celery_app import celery
from app.tasks.reminders.bookings import remind_of_booking


@celery.task(name="email.booking_reminder_1day")
def remind_booking_1day():
    asyncio.run(remind_of_booking(1))


@celery.task(name="email.booking_reminder_3days")
def remind_booking_3day():
    asyncio.run(remind_of_booking(3))


# @celery.task(name="periodic_task")
# def periodic_task():
#     print(12345)
