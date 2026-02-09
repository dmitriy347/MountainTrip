import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTripMediaEndpoint:
    """Тесты GET /api/trips/{id}/media/"""

    def test_trip_media_empty_list(self, api_client, trip):
        """Получение пустого списка медиафайлов."""
        url = reverse("trip-media", kwargs={"pk": trip.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
        assert len(response.data) == 0

    def test_trip_media_not_found(self, api_client):
        """Несуществующая поездка -> 404."""
        url = reverse("trip-media", kwargs={"pk": 999})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
