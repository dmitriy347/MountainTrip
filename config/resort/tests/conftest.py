import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from resort.models import Resort, Trip, TripMedia


User = get_user_model()

# Используем pytest fixtures для создания тестовых данных

@pytest.fixture
def user(db):
    """Обычный авторизованный пользователь"""
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )


@pytest.fixture
def another_user(db):
    """Другой пользователь (для проверки прав доступа)"""
    return User.objects.create_user(
        username="anotheruser",
        email="another@example.com",
        password="password123"
    )


@pytest.fixture
def resort(db):
    """Курорт с дефолтными значениями"""
    return Resort.objects.create(
        name="Test Resort",
        region="Test Region",
        description="Test description",
        slug="test-resort"
    )


@pytest.fixture
def resort_with_custom_slug(db):
    """Курорт с кастомным slug (для тестов urls / 404)"""
    return Resort.objects.create(
        name="Another Resort",
        region="Another Region",
        description="Another description",
        slug="another-resort"
    )


@pytest.fixture
def trip(db, user, resort):
    """Поездка пользователя на курорт"""
    return Trip.objects.create(
        user=user,
        resort=resort,
        start_date="2023-12-01",
        end_date="2023-12-10",
        is_public=False
    )


@pytest.fixture
def public_trip(another_user, resort):
    """Публичная поездка другого пользователя"""
    return Trip.objects.create(
        user=another_user,
        resort=resort,
        start_date="2023-11-01",
        end_date="2023-11-05",
        is_public=True
    )


@pytest.fixture
def image_file():
    """Фикстура для создания тестового изображения"""
    return SimpleUploadedFile(
        name='test.jpg',
        content=b'filecontent',
        content_type='image/jpeg'
    )


@pytest.fixture
def trip_media(db, trip, image_file):
    """Медиафайл, связанный с поездкой"""
    return TripMedia.objects.create(
        trip=trip,
        image=image_file
    )


@pytest.fixture
def auth_client(client, user):
    """Django test client с авторизованным пользователем"""
    client.login(username="testuser", password="password123")
    return client