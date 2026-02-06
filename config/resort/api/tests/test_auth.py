import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAuthentication:
    """Тесты аутентификации JWT."""

    def test_obtain_token_success(self, api_client, user):
        """Успешное получение токена с валидными учетными данными."""
        url = reverse("token_obtain_pair")
        data = {
            "username": user.username,
            "password": "testpass123",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert len(response.data["access"]) > 50

    def test_obtain_token_invalid_credentials(self, api_client, user):
        """Неверные учетные данные не должны выдавать токен."""
        url = reverse("token_obtain_pair")
        data = {
            "username": user.username,
            "password": "wrongpassword",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "access" not in response.data
        assert "refresh" not in response.data

    def test_refresh_token_success(self, api_client, user_token):
        """Успешное обновление access токена"""
        url = reverse("token_refresh")
        data = {
            "refresh": user_token["refresh"],
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

        # Новый access токен отличается от старого
        assert response.data["access"] != user_token["access"]

    def test_refresh_token_invalid(self, api_client, user_token):
        """Невалидный refresh токен не должен выдавать новый access токен"""
        url = reverse("token_refresh")
        data = {
            "refresh": "invalidtoken",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "access" not in response.data
