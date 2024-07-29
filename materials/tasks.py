from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from users.models import User


@shared_task
def send_info(course, recipients, message):
    send_mail(f'Курс {course} обновлен', message,
              EMAIL_HOST_USER, recipients)


@shared_task
def deactivate_user():
    today = timezone.now().date()
    for u in User.objects.all():
        if u.last_login and u.last_login.date() + timedelta(days=30) < today:
            u.is_active = False
            u.save()
