import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from resort.models import Resort, Trip


@pytest.fixture
def api_client():
    """Клиент для отправки API-запросов."""
    return APIClient()


@pytest.fixture
def user():
    """Создание тестового пользователя."""
    return User.objects.create_user(
        username="testuser", password="testpass123", email="test@example.com"
    )


@pytest.fixture
def another_user():
    """Создание второго тестового пользователя."""
    return User.objects.create_user(
        username="anotheruser", password="testpass123", email="another@example.com"
    )


@pytest.fixture
def user_token(user):
    """Генерация JWT токена для тестового пользователя."""
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


@pytest.fixture
def authenticated_client(api_client, user_token):
    """API клиент с авторизацией."""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token['access']}")
    return api_client


@pytest.fixture
def resort():
    """Создание тестового курорта."""
    return Resort.objects.create(
        name="Роза Хутор",
        region="Краснодарский край",
        description="Тестовое описание",
        slug="roza-hutor",
    )


@pytest.fixture
def another_resort():
    """Создание второго тестового курорта."""
    return Resort.objects.create(
        name="Шерегеш",
        region="Кемеровская область",
        description="Горнолыжный курорт",
        slug="sheregesh",
    )


@pytest.fixture
def trip(user, resort):
    """Создание публичной поездки."""
    return Trip.objects.create(
        user=user,
        resort=resort,
        start_date="2024-01-10",
        end_date="2024-01-17",
        comment="Публичная поездка!",
        is_public=True,
    )


@pytest.fixture
def private_trip(user, resort):
    """Создание приватной поездки."""
    return Trip.objects.create(
        user=user,
        resort=resort,
        start_date="2024-02-10",
        end_date="2024-02-17",
        comment="Приватная поездка",
        is_public=False,
    )


@pytest.fixture
def another_user_trip(another_user, resort):
    """Создание поездки другого пользователя."""
    return Trip.objects.create(
        user=another_user,
        resort=resort,
        start_date="2024-03-10",
        end_date="2024-03-17",
        comment="Чужая публичная поездка",
        is_public=True,
    )
