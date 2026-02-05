from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from resort.models import Resort, Trip, TripMedia
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import ResortFilter
from .serializers import (
    ResortSerializer,
    TripSerializer,
    TripMediaSerializer,
    UserSerializer,
)
from rest_framework.filters import OrderingFilter, SearchFilter


class ResortViewSet(ReadOnlyModelViewSet):
    """ViewSet для модели Resort."""

    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ResortFilter  # Кастомный фильтр для курортов
    ordering_fields = ["name", "region"]  # Разрешенные поля для сортировки
    ordering = ["name"]  # Сортировка по умолчанию
    search_fields = ["name", "region", "description"]  # Поля для поиска

    @action(detail=True, methods=["get"])
    def trips(self, request, slug=None):
        """
        Вложенный эндпоинт: GET /api/resorts/{slug}/trips/
        Возвращает поездки на конкретный курорт.

        Права доступа:
        - Неавторизованные: только чтение (GET) публичных поездок
        - Авторизованные: чтение публичных + в будущем CRUD своих поездок
        """
        # Получаем текущий курорт по slug из URL
        resort = self.get_object()

        # Получаем все поездки, связанные с курортом
        trips = resort.trips.all()

        user = self.request.user
        if user.is_authenticated:
            # Авторизованный: показываем публичные + свои приватные поездки
            trips = trips.filter(Q(is_public=True) | Q(user=user)).select_related(
                "user"
            )
        else:
            # Гость: показываем только публичные поездки
            trips = trips.filter(is_public=True).select_related("user")

        serializer = TripSerializer(trips, many=True, context={"request": request})
        return Response(serializer.data)


class TripViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для модели Trip.

    Права доступа:
    - Неавторизованные: только чтение (GET) публичных поездок
    - Авторизованные: чтение публичных + в будущем CRUD своих поездок
    """

    serializer_class = TripSerializer

    # Не авторизованные - только GET, авторизованные - CRUD
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["is_public", "resort"]  # Разрешенные поля для фильтрации
    ordering_fields = ["start_date", "end_date"]  # Разрешенные поля для сортировки
    ordering = ["-start_date"]  # Сортировка по умолчанию
    search_fields = ["resort__name", "resort__region", "comment"]  # Поля для поиска

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
            # Не авторизованный: только публичные
            return (
                Trip.objects.filter(is_public=True)
                .select_related("user", "resort")
                .prefetch_related("media")
            )

    @action(detail=True, methods=["get"])
    def media(self, request, pk=None):
        """
        Вложенный эндпоинт: GET /api/trips/{id}/media/
        Возвращает медиафайлы, связанные с конкретной поездкой.
        """
        trip = self.get_object()
        media_files = trip.media.all()

        # context нужен для правильного формирования абсолютных URL изображений
        serializer = TripMediaSerializer(
            media_files, many=True, context={"request": request}
        )
        return Response(serializer.data)


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


class UserViewSet(ReadOnlyModelViewSet):
    """ViewSet для профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def trips(self, request, pk=None):
        """
        Вложенный эндпоинт: GET /api/users/{id}/trips/
        Возвращает публичные поездки пользователя.
        """
        user = self.get_object()
        trips = user.trips.filter(is_public=True).select_related("resort")

        serializer = TripSerializer(trips, many=True, context={"request": request})
        return Response(serializer.data)
