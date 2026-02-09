from django.contrib.auth.models import User
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from resort.models import Resort, Trip, TripMedia
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .filters import ResortFilter, TripFilter
from .permissions import IsOwnerReadOnly
from .serializers import (
    ResortSerializer,
    TripReadSerializer,
    TripWriteSerializer,
    TripMediaSerializer,
    UserSerializer,
)
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        summary="Список курортов",
        description="Получить список всех горнолыжных курортов с пагинацией, фильтрацией и поиском.",
        tags=['resorts']
    ),
    retrieve=extend_schema(
        summary="Детали курорта",
        description="Получить подробную информацию о конкретном курорте по slug.",
        tags=['resorts']
    ),
    trips=extend_schema(
        summary="Поездки на курорт",
        description="Получить список поездок на конкретный курорт. Гости видят только публичные поездки, авторизованные пользователи видят публичные + свои приватные.",
        tags=['resorts']
    ),
)
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

        serializer = TripReadSerializer(trips, many=True, context={"request": request})
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Список поездок",
        description="Получить список поездок с фильтрацией, поиском и сортировкой. Гости видят только публичные, авторизованные видят публичные + свои.",
        tags=['trips']
    ),
    retrieve=extend_schema(
        summary="Детали поездки",
        description="Получить подробную информацию о конкретной поездке.",
        tags=['trips']
    ),
    create=extend_schema(
        summary="Создать поездку",
        description="Создать новую поездку. Требуется аутентификация. User автоматически берётся из токена.",
        tags=['trips']
    ),
    update=extend_schema(
        summary="Обновить поездку (полностью)",
        description="Полное обновление поездки (PUT). Только владелец может обновить свою поездку.",
        tags=['trips']
    ),
    partial_update=extend_schema(
        summary="Обновить поездку (частично)",
        description="Частичное обновление поездки (PATCH). Можно обновить только нужные поля. Только владелец.",
        tags=['trips']
    ),
    destroy=extend_schema(
        summary="Удалить поездку",
        description="Удалить поездку. Только владелец может удалить свою поездку.",
        tags=['trips']
    ),
    media=extend_schema(
        summary="Фото поездки",
        description="Получить список фотографий конкретной поездки.",
        tags=['trips']
    ),
)
class TripViewSet(ModelViewSet):
    """
    ViewSet для поездок из модели Trip с полным CRUD.

    Права доступа:
    - GET: все пользователи (публичные поездки + свои)
    - POST: только авторизованные
    - PUT/PATCH: только владелец поездки
    - DELETE: только владелец поездки
    """

    # Не авторизованные - только GET, авторизованные - CRUD
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = TripFilter  # Кастомный фильтр для поездок
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

    def get_serializer_class(self):
        """Используем разные serializers для чтения (GET) и записи (POST/PUT/PATCH)."""
        if self.action in ["create", "update", "partial_update"]:
            return TripWriteSerializer
        return TripReadSerializer

    def perform_create(self, serializer):
        """При создании поездки автоматически привязываем текущего пользователя."""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Переопределяем create для использования TripReadSerializer в ответе."""
        # Используем TripWriteSerializer для валидации
        write_serializer = self.get_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)

        # Сохраняем поездку с текущим пользователем
        self.perform_create(write_serializer)

        # Получаем созданный объект поездки
        instance = write_serializer.instance

        # Сериализуем его через TripReadSerializer для ответа
        read_serializer = TripReadSerializer(instance, context={"request": request})

        # Возвращаем ответ с полными данными новой поездки
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Переопределяем update для использования TripReadSerializer в ответе."""
        partical = kwargs.pop("partial", False)  # PUT или PATCH

        # Получаем текущий объект поездки
        instance = self.get_object()

        # Валидация через TripWriteSerializer
        write_selializer = self.get_serializer(
            instance, data=request.data, partial=partical
        )
        write_selializer.is_valid(raise_exception=True)
        self.perform_update(write_selializer)

        # Проверка на устаревшие данные
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        # Сериализуем обновленный объект через TripReadSerializer для ответа
        read_serializer = TripReadSerializer(instance, context={"request": request})
        return Response(read_serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Переопределяем partial_update для использования TripReadSerializer"""
        kwargs["partial"] = True  # PATCH
        return self.update(request, *args, **kwargs)

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

        serializer = TripReadSerializer(trips, many=True, context={"request": request})
        return Response(serializer.data)
