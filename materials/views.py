from rest_framework import viewsets, generics

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseLessonsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return CourseLessonsSerializer
        return CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
