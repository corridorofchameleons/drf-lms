from django.urls import path

from users.apps import UsersConfig
from users.views import UserRetrieveUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('<int:pk>/', UserRetrieveUpdateAPIView.as_view()),
]
