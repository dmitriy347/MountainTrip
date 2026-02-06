import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestTrips:
    """Тесты GET /api/trips/"""

    def test_guest_sees_only_public_trips(self, api_client, trip, private_trip):
        """Гость видит только публичные поездки."""
        url = reverse("trip-list")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == trip.id

    def test_authenticated_user_sees_own_and_public_trips(
        self, authenticated_client, trip, private_trip, another_user_trip
    ):
        """Авторизованный видит свои (в т.ч. приватные) и публичные поездки других."""
        url = reverse("trip-list")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Должен видеть 3 поездки: свою публичную, свою приватную, и чужую публичную
        assert len(response.data["results"]) == 3

        trip_ids = {t["id"] for t in response.data["results"]}
        assert trip.id in trip_ids  # Своя публичная
        assert private_trip.id in trip_ids  # Своя приватная
        assert another_user_trip.id in trip_ids  # Чужая публичная


@pytest.mark.django_db
class TestTripDetail:
    """Тесты GET /api/trips/{id}/"""

    def test_get_public_trip_as_guest(self, api_client, trip):
        """Гость может видеть публичную поездку."""
        url = reverse("trip-detail", kwargs={"pk": trip.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == trip.id
        assert response.data["user"] == trip.user.username
        assert "resort" in response.data
        assert response.data["resort"]["name"] == trip.resort.name

    def test_get_private_trip_as_guest(self, api_client, private_trip):
        """Гость не может видеть приватную поездку."""
        url = reverse("trip-detail", kwargs={"pk": private_trip.id})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

