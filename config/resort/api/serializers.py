from rest_framework import serializers
from resort.models import Resort, Trip


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
