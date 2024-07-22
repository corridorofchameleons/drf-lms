from django.urls import path, include
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonListAPIView, LessonUpdateAPIView, LessonDestroyAPIView, \
    LessonRetrieveAPIView, LessonCreateAPIView, SubscriptionView

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path('courses/', include(router.urls)),

    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_details'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson_list'),

    path('subscriptions/', SubscriptionView.as_view())
]
