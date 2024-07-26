from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=40, unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    town = models.CharField(max_length=50, verbose_name='Город', null=True)
    img = models.ImageField(upload_to='users/imgs', null=True, blank=True, verbose_name='Аватар')
    # token = models.CharField(max_length=100, verbose_name='Токен', default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    PAYMENT_TYPES = (
        ('c', 'cash'),
        ('t', 'transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    payment_type = models.CharField(max_length=1, choices=PAYMENT_TYPES, default='t', verbose_name='Тип оплаты')
    payment_link = models.CharField(max_length=400, null=True)
    session_id = models.CharField(max_length=100, null=True)

    # создадим полиморфную связь
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    def __str__(self):
        return f'{self.user}, {self.payment_date} - {self.content_object}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
