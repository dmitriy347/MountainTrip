import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserTripEndpoint:
    """Тесты GET /api/users/{id}/trips/"""

    def test_user_public_trips_as_guest(self, api_client, user, trip, private_trip):
        """Гость видит только публичные поездки пользователя."""
        url = reverse("user-trips", kwargs={"pk": user.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == trip.id

    def test_user_trips_not_found(self, api_client):
        """Несуществующий пользователь -> 404."""
        url = reverse("user-trips", kwargs={"pk": 999})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
