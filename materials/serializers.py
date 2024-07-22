from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_link


class LessonSerializer(serializers.ModelSerializer):
    link = serializers.CharField(validators=[validate_link])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseLessonsSerializer(serializers.ModelSerializer):
    lessons_num = SerializerMethodField()
    lessons = LessonSerializer(many=True)
    subscription = SerializerMethodField()

    def get_subscription(self, course):
        user = self.context.get('request').user
        return Subscription.objects.filter(user=user, course=course).exists()

    def get_lessons_num(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = ['name', 'img', 'description', 'lessons_num', 'subscription', 'lessons']
