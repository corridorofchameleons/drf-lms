from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import generics, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson
from users.models import User, Payment
from users.permissions import IsSelf
from users.serializers import UserSerializer, PaymentSerializer, UserMiniSerializer, PaymentPostSerializer
from users.services import create_session


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
    serializer_class = PaymentPostSerializer
    queryset = Payment.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        obj_id = serializer.validated_data.get('object_id')
        cont_type = serializer.validated_data.get('content_type').pk

        if Payment.objects.filter(user=user, object_id=obj_id,
                                  content_type=cont_type).exists():
            return Response({"message": 'already exists'})

        payment = serializer.save(user=user)

        try:
            if cont_type == 7:
                name = Course.objects.get(pk=obj_id)
            elif cont_type == 8:
                name = Lesson.objects.get(pk=obj_id)
            else:
                raise Http404('Nothing like that')
        except:
            raise Http404('Nothing like that')

        session_id, payment_link = create_session(100000, name)
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()

        return Response({"payment_link": payment_link})
