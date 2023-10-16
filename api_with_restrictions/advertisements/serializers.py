from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError

from advertisements.models import Advertisement, Favorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        user = self.context['request'].user
        if data.get('status'):
            if data['status'] == 'OPEN':
                if Advertisement.objects.filter(
                        creator=user, status='OPEN').count() >= 10:
                    raise ValidationError('Не больше 10 открытых объявлений!')
        return data


class FavoritesSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementSerializer(
        read_only=True,
    )

    class Meta:
        model = Favorite
        fields = ('id', 'advertisement')

    def validate(self, data):
        return data
