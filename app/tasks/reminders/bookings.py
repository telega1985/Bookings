import smtplib
from app.logger import logger
from app.config import settings

from app.bookings.service import BookingService
from app.tasks.email_templates import create_booking_reminder_template


async def remind_of_booking(days: int):
    """
    Отправляет email'ы с напоминанием о забронированном номере за days дней
    """
    bookings = await BookingService.service_find_need_to_remind(days)
    logger.info(f"{bookings=}")

    msgs = []

    for booking in bookings:
        email_to = booking.user.email
        booking_data = {
            "date_from": booking.date_from,
            "date_to": booking.date_to
        }
        msg_content = create_booking_reminder_template(booking_data, email_to, days)
        msgs.append(msg_content)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        for msg_content in msgs:
            server.send_message(msg_content)

    logger.info("Successfully sent reminding messages")
