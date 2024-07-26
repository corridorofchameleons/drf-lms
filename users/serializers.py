from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['content_type', 'object_id']


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name']
