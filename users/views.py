from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from materials.models import Course, Lesson
from users.models import User, Payment
from users.permissions import IsSelf
from users.serializers import UserSerializer, PaymentSerializer, UserMiniSerializer
from users.services import create_session, create_price


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


class PaymentAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        payment = serializer.save(user=user)
        obj = payment.content_type.pk
        try:
            if obj == 7:
                name = Course.objects.get(pk=payment.object_id)
            elif obj == 8:
                name = Lesson.objects.get(pk=payment.object_id)
            else:
                raise Http404('Nothing like that')
        except:
            raise Http404('Nothing like that')
        # print(obj)
        session_id, payment_link = create_session(100000, name)
        print(session_id, payment_link)
        payment.save()
