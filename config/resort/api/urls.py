from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

from .views import ResortViewSet, TripViewSet, TripMediaViewSet, UserViewSet

router = DefaultRouter()
router.register(r"resorts", ResortViewSet, basename="resort")
router.register(r"trips", TripViewSet, basename="trip")
router.register(r"media", TripMediaViewSet, basename="tripmedia")
router.register(r"users", UserViewSet, basename="user")

# Оборачиваем JWT эндпоинты в extend_schema для документации
urlpatterns = [
    # JWT эндпоинты
    path(
        "auth/token/",
        extend_schema(
            tags=["auth"],
            summary='Получить JWT токены',
            description='Аутентификация пользователя. Возвращает access и refresh токены.',
        )(TokenObtainPairView.as_view()),
        name="token_obtain_pair"
    ),
    path(
        "auth/token/refresh/",
        extend_schema(
            tags=['auth'],
            summary='Обновить access токен',
            description='Обновить истёкший access токен, используя refresh токен.',
        )(TokenRefreshView.as_view()),
        name="token_refresh"
    ),
] + router.urls
