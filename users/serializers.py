from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """Сериализатор модели Платежи"""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Сериализатор модели Пользователь"""

    payment_history = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
