from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса')
    img = models.ImageField(upload_to='courses/', verbose_name='Картинка')
    description = models.TextField(verbose_name='Описание курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название урока')
    img = models.ImageField(upload_to='lessons/', verbose_name='Картинка')
    description = models.TextField(verbose_name='Описание урока')
    link = models.CharField(max_length=200, verbose_name='Ссылка')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
