from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseLessonsNumSerializer(serializers.ModelSerializer):
    lessons_num = SerializerMethodField()

    def get_lessons_num(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ['name', 'img', 'description', 'lessons_num']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
