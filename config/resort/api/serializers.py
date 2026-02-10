from django.contrib.auth.models import User
from rest_framework import serializers
from resort.models import Resort, Trip, TripMedia


class ResortSerializer(serializers.ModelSerializer):
    """Serializer для отображения курортов из модели Resort."""

    class Meta:
        model = Resort
        fields = ["id", "name", "slug", "region", "description", "created_at"]
        read_only_fields = ["id", "slug", "created_at"]


class TripWriteSerializer(serializers.ModelSerializer):
    """Serializer для создания и обновления поездок из модели Trip."""

    class Meta:
        model = Trip
        fields = [
            "resort",  # Ожидаем ID курорта
            "start_date",
            "end_date",
            "comment",
            "is_public",
        ]

    def validate(self, data):
        """
        Валидация: дата начала не может быть позже даты окончания.
        Работает для POST (создание), и для PUT/PATCH (полное/частичное обновление).
        """

        # Получаем start_date и end_date из данных для валидации
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        # Если это PUT/PATCH-запрос (instance уже существует)
        if self.instance:
            # Если start_date или end_date не переданы - значит это PATCH
            if start_date is None:
                # Используем существующее значение из текущего объекта
                start_date = self.instance.start_date
            if end_date is None:
                end_date = self.instance.end_date

        # Проверяем только если оба поля известны
        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError(
                    "Дата начала не может быть позже даты окончания."
                )
        return data


class TripReadSerializer(serializers.ModelSerializer):
    """Serializer для отображения поездок из модели Trip."""

    # Отображение пользователя по его строковому представлению
    user = serializers.StringRelatedField()
    resort = ResortSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "user",
            "resort",  # Ожидаем вложенный объект курорта
            "start_date",
            "end_date",
            "comment",
            "is_public",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class TripMediaSerializer(serializers.ModelSerializer):
    """Serializer для отображения медиа из модели TripMedia."""

    # Показать только trip_id, а не весь объект
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TripMedia
        fields = ["id", "trip", "image", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class UserSerializer(serializers.ModelSerializer):
    """Serializer для отображения профиля пользователя."""

    trips_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "date_joined", "trips_count"]
        read_only_fields = ["id", "username", "date_joined"]

    def get_trips_count(self, obj):
        """Возвращает количество поездок пользователя."""
        return obj.trips.filter(is_public=True).count()
