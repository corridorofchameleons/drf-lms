from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=40, unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    country = models.CharField(max_length=50, verbose_name='Страна')
    img = models.ImageField(upload_to='users/imgs', null=True, blank=True, verbose_name='Аватар')
    token = models.CharField(max_length=100, verbose_name='Токен', default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
