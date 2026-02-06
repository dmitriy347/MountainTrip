import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestResortList:
    """Тесты GET /api/resorts/"""

    def test_list_resorts(self, api_client, resort, another_resort):
        """Список курортов доступен всем."""
        url = reverse("resort-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

        # Проверяем структуру данных
        resort_data = response.data["results"][0]
        assert "id" in resort_data
        assert "name" in resort_data
        assert "slug" in resort_data
        assert "region" in resort_data
        assert "description" in resort_data

    def test_list_resorts_empty(self, api_client):
        """Пустой список курортов."""
        url = reverse("resort-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 0
