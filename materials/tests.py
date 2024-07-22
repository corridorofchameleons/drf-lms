from rest_framework.test import APITestCase
from rest_framework.serializers import ValidationError
from materials.models import Course, Lesson, Subscription
from users.models import User

from django.shortcuts import reverse
from rest_framework import status


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@kremlin.ru")
        self.course = Course.objects.create(name="Новый курс", description="Описание")
        self.lesson = Lesson.objects.create(name="Новый урок", description="Описание",
                                            link="link.youtube.com", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson_details', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse('materials:lesson_create')
        data = {
            "name": "Урок 1",
            "course": self.course.pk,
            "description": "Описание",
            "link": "my_link.youtube.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

        data = {
            "name": "Урок 1",
            "course": self.course.pk,
            "description": "Описание",
            "link": "my_link.rutube.ru"
        }
        self.assertRaises(ValidationError)

    def test_lesson_update(self):
        url = reverse('materials:lesson_update', args=(self.lesson.pk,))
        data = {
            "name": "Урок 2"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('name'), "Урок 2"
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

    def test_lesson_list(self):
        url = reverse('materials:lesson_list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': self.lesson.pk, 'link': self.lesson.link, 'name': self.lesson.name, 'img': self.lesson.img,
             'description': self.lesson.description, 'course': self.lesson.course.pk,
             'owner': self.lesson.owner.pk}]}

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@kremlin.ru")
        self.course = Course.objects.create(name="Новый курс", description="Описание")
        self.client.force_authenticate(user=self.user)

    def test_subscrtiption_post(self):
        url = reverse('materials:subscribe')
        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.data.get('message'), 'subscription created'
        )
        response = self.client.post(url, data)
        self.assertEqual(
            response.data.get('message'), 'subscription deleted'
        )
        response = self.client.post(url, data)
        self.assertEqual(
            response.data.get('message'), 'subscription created'
        )
