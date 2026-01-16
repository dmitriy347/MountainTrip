import pytest
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from datetime import date


from resort.models import Resort, Trip, TripMedia


User = get_user_model()

# Используем pytest fixtures для создания тестовых данных
# Общие фикстуры для тестов: пользователи, курорт, поездка, image и клиент.


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
    """Тестовый курорт с дефолтными значениями"""
    return Resort.objects.create(
        name="Test Resort",
        region="Test Region",
        description="Test description",
    )


@pytest.fixture
def another_resort(db):
    """Другой курорт (для проверки разных поездок)"""
    return Resort.objects.create(
        name="Another Resort",
        region="Another Region",
        description="Another description",
    )


@pytest.fixture
def trip(db, user, resort):
    """Поездка пользователя на тестовый курорт"""
    return Trip.objects.create(
        user=user,
        resort=resort,
        start_date=date(2023, 12, 1),
        end_date=date(2023, 12, 10),
        is_public=False
    )


@pytest.fixture
def trip_invalid(db, user, resort):
    """Поездка пользователя с некорректными датами (для теста валидации)"""
    return Trip(
        user=user,
        resort=resort,
        start_date=date(2023, 12, 10),
        end_date=date(2023, 12, 1),
        is_public=False
    )


@pytest.fixture
def public_trip_another_user(another_user, another_resort):
    """Публичная поездка другого пользователя на другой курорт"""
    return Trip.objects.create(
        user=another_user,
        resort=another_resort,
        start_date=date(2023, 11, 1),
        end_date=date(2023, 11, 5),
        is_public=True
    )

@pytest.fixture
def private_trip_another_user(another_user, another_resort):
    """Приватная поездка другого пользователя на другой курорт"""
    return Trip.objects.create(
        user=another_user,
        resort=another_resort,
        start_date=date(2023, 10, 1),
        end_date=date(2023, 10, 5),
        is_public=False
    )


@pytest.fixture
def public_trip_another_user_resort(resort, another_user):
    """Публичная поездка другого пользователя на тестовый курорт"""
    return Trip.objects.create(
        user=another_user,
        resort=resort,
        start_date=date(2023, 9, 1),
        end_date=date(2023, 9, 5),
        is_public=True
    )


@pytest.fixture
def private_trip_another_user_resort(resort, another_user):
    """Приватная поездка другого пользователя на тестовый курорт"""
    return Trip.objects.create(
        user=another_user,
        resort=resort,
        start_date=date(2023, 8, 1),
        end_date=date(2023, 8, 5),
        is_public=False
    )


@pytest.fixture
def image_file():
    """Создание тестового минимально-валидного изображения в памяти"""
    image = Image.new('RGB', (10, 10), color = 'white')
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile(name="test_image.jpg", content=buffer.read(), content_type="image/jpeg")


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