import smtplib
from app.tasks.celery_app import celery
from app.config import settings
from PIL import Image
from pathlib import Path
from pydantic import EmailStr

from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(path: str):
    """
    Обработка картинок
    """
    directory_path = "app/static/images"
    im_path = Path(path) # app/static/images/1.webp
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000, 500))
    im_resized_200_100 = im.resize((200, 100))
    im_resized_1000_500.save(f"{directory_path}/resized_1000_500_{im_path.name}")
    im_resized_200_100.save(f"{directory_path}/resized_200_100_{im_path.name}")


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    """
    Отправка письма пользователю
    """
    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
