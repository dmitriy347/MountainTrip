from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from resort.models import Resort, Trip, TripMedia
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ResortSerializer, TripSerializer, TripMediaSerializer
from rest_framework.filters import OrderingFilter


class ResortViewSet(ReadOnlyModelViewSet):
    """ViewSet для модели Resort."""

    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    lookup_field = "slug"
    filter_backends = [OrderingFilter]
    ordering_fields = ["name", "region"]  # Разрешенные поля для сортировки
    ordering = ["name"]  # Сортировка по умолчанию

    def get_queryset(self):
        queryset = Resort.objects.all()
        region = self.request.query_params.get("region")
        if region:
            queryset = queryset.filter(region__icontains=region)
        return queryset


class TripViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для модели Trip.

    Права доступа:
    - Неавторизованные: только чтение (GET) публичных поездок
    - Авторизованные: чтение публичных + в будущем CRUD своих поездок
    """

    serializer_class = TripSerializer

    # Гости - только GET, авторизованные - CRUD
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [OrderingFilter]
    ordering_fields = ["start_date", "end_date"]  # Разрешенные поля для сортировки
    ordering = ["-start_date"]  # Сортировка по умолчанию

    def get_queryset(self):
        """Фильтрация поездок в зависимости от авторизации пользователя."""
        user = self.request.user
        if user.is_authenticated:
            # Авторизованный: публичные + свои приватные
            return (
                Trip.objects.filter(Q(is_public=True) | Q(user=user))
                .select_related("user", "resort")
                .prefetch_related("media")
            )
        else:
            # Гость: только публичные
            return (
                Trip.objects.filter(is_public=True)
                .select_related("user", "resort")
                .prefetch_related("media")
            )


class TripMediaViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для модели TripMedia.

    Права доступа:
    - Неавторизованные: только чтение (GET) фото публичных поездок
    - Авторизованные: чтение фото публичных поездок + в будущем CRUD фото своих поездок
    """

    serializer_class = TripMediaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Фильтрация медиафайлов в зависимости от авторизации пользователя."""
        user = self.request.user
        if user.is_authenticated:
            # Авторизованный: медиа публичных поездок + своих приватных поездок
            return TripMedia.objects.filter(
                Q(trip__is_public=True) | Q(trip__user=user)
            ).select_related("trip")
        else:
            # Гость: только медиа публичных поездок
            return TripMedia.objects.filter(trip__is_public=True).select_related("trip")
