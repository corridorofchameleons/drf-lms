from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


@shared_task
def send_info(course, recipients, message):
    send_mail(f'Курс {course} обновлен', message,
              EMAIL_HOST_USER, recipients)
