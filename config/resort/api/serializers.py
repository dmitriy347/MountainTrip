from django.contrib.auth.models import User
from rest_framework import serializers
from resort.models import Resort, Trip, TripMedia


class ResortSerializer(serializers.ModelSerializer):
    """Serializer для модели Resort."""

    class Meta:
        model = Resort
        fields = ["id", "name", "slug", "region", "description", "created_at"]
        read_only_fields = ["id", "slug", "created_at"]


class TripSerializer(serializers.ModelSerializer):
    """Serializer для модели Trip."""

    # Отображение пользователя по его строковому представлению
    user = serializers.StringRelatedField()
    resort = ResortSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "user",
            "resort",
            "start_date",
            "end_date",
            "comment",
            "is_public",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class TripMediaSerializer(serializers.ModelSerializer):
    """Serializer для модели TripMedia."""

    # Показать только trip_id, а не весь объект
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TripMedia
        fields = ["id", "trip", "image", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer для профиля пользователя."""

    trips_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "date_joined", "trips_count"]
        read_only_fields = ["id", "username", "date_joined"]

    def get_trips_count(self, obj):
        """Возвращает количество поездок пользователя."""
        return obj.trips.filter(is_public=True).count()
