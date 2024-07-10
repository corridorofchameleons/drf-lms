from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserPaymentsAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('content_type', 'payment_type')
    ordering_fields = ('payment_date',)
