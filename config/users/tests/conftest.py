import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    """Обычный пользователь для тестов"""
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def auth_client(client, user):
    """Django test client с авторизованным пользователем"""
    client.login(username="testuser", password="testpass123")
    return client
