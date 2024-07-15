from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.permissions import IsSelf
from users.serializers import UserSerializer, PaymentSerializer, UserMiniSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny,

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsSelf, IsAuthenticated


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserMiniSerializer
    permission_classes = IsAuthenticated,


class UserPaymentsAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('content_type', 'payment_type')
    ordering_fields = ('payment_date',)
