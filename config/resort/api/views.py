from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from resort.models import Resort, Trip
from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ResortSerializer, TripSerializer
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
    - Авторизованные: чтение всех + в будущем CRUD своих поездок
    """

    serializer_class = TripSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Гости - только GET, авторизованные - CRUD

    filter_backends = [OrderingFilter]
    ordering_fields = ["start_date", "end_date"]  # Разрешенные поля для сортировки
    ordering = ["-start_date"]  # Сортировка по умолчанию

    def get_queryset(self):
        """Фильтрация поездок в зависимости от авторизации пользователя."""
        user = self.request.user
        if user.is_authenticated:
            # Авторизованный: публичные + свои приватные
            return Trip.objects.filter(
                Q(is_public=True) | Q(user=user)
            ).select_related("user", "resort").prefetch_related("media")
        else:
            # Гость: только публичные
            return Trip.objects.filter(is_public=True).select_related(
                "user", "resort"
            ).prefetch_related("media")