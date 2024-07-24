from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    UserRetrieveUpdateDestroyAPIView,
    UserPaymentsAPIView,
    UserCreateAPIView,
    UserListAPIView, PaymentAPIView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('payments/', UserPaymentsAPIView.as_view()),
    path('payment/', PaymentAPIView.as_view()),
    path('users/', UserListAPIView.as_view()),

    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]
