from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.shortcuts import get_object_or_404
from django.http import Http404

from materials.models import Course, Lesson, Subscription
from materials.pagination import MyPaginator
from materials.serializers import CourseSerializer, LessonSerializer, CourseLessonsSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MyPaginator

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()

        # здесь тоже придется изменить
        # return Course.objects.filter(owner=user)
        return Course.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return CourseLessonsSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModerator, IsAuthenticated]
        # временно пока сделаем так
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ('retrieve', 'update'):
            self.permission_classes = [IsModerator | IsOwner, IsAuthenticated]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner, IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MyPaginator

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionView(APIView):
    @swagger_auto_schema(operation_description="Enables or disables subscription",
                         manual_parameters=[Parameter('course_id', IN_QUERY, type='int')],
                         responses={200: "Subscription created, Subscription deleted", 404: "No Course matches the "
                                                                                            "given query."})
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        try:
            subscr = get_object_or_404(Subscription, course=course, user=user)
            subscr.delete()
            message = 'subscription deleted'
        except Http404:
            Subscription.objects.create(user=user, course=course)
            message = 'subscription created'

        return Response({"message": message})
