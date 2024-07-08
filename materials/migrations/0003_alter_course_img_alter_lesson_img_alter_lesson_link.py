# Generated by Django 5.0.6 on 2024-07-08 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_lesson_course_lesson_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='img',
            field=models.ImageField(null=True, upload_to='courses/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='img',
            field=models.ImageField(null=True, upload_to='lessons/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='link',
            field=models.CharField(max_length=200, null=True, verbose_name='Ссылка'),
        ),
    ]
