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


@pytest.mark.django_db
class TestTripCreate:
    """Тесты POST /api/trips/"""

    def test_create_trip_as_guest(self, api_client, resort):
        """Гость не может создавать поездку."""
        url = reverse("trip-list")
        data = {
            "resort": resort.id,
            "start_date": "2024-04-01",
            "end_date": "2024-04-07",
            "comment": "Новая поездка",
            "is_public": True,
        }

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_trip_as_authenticated_user(
        self, authenticated_client, user, resort
    ):
        """Авторизованный может создавать поездку."""
        url = reverse("trip-list")
        data = {
            "resort": resort.id,
            "start_date": "2024-04-01",
            "end_date": "2024-04-07",
            "comment": "Новая поездка",
            "is_public": True,
        }

        response = authenticated_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"] == user.username
        assert response.data["resort"]["id"] == resort.id
        assert response.data["start_date"] == "2024-04-01"
        assert response.data["comment"] == "Новая поездка"

    def test_create_trip_with_invalid_dates(self, authenticated_client, resort):
        """Невалидные даты: start_date > end_date."""
        url = reverse("trip-list")
        data = {
            "resort": resort.id,
            "start_date": "2024-04-10",
            "end_date": "2024-04-01",
            "comment": "Невалидные даты",
            "is_public": True,
        }

        response = authenticated_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data


@pytest.mark.django_db
class TestTripUpdate:
    """Тесты PUT/PATCH /api/trips/{id}/"""

    def test_update_own_trip(self, authenticated_client, trip):
        """Пользователь может обновлять свою поездку."""
        url = reverse("trip-detail", kwargs={"pk": trip.id})
        data = {
            "resort": trip.resort.id,
            "start_date": trip.start_date,
            "end_date": "2024-05-07",
            "comment": "Обновленная поездка",
            "is_public": True,
        }

        response = authenticated_client.put(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["end_date"] == "2024-05-07"
        assert response.data["comment"] == "Обновленная поездка"

    def test_partial_update_own_trip(self, authenticated_client, trip):
        """PATCH обновляет только указанные поля."""
        url = reverse("trip-detail", kwargs={"pk": trip.id})
        data = {"comment": "Частично обновленная поездка"}

        response = authenticated_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["comment"] == "Частично обновленная поездка"
        assert response.data["start_date"] == str(trip.start_date)  # Не изменилось

    def test_update_another_user_trip(self, authenticated_client, another_user_trip):
        """Нельзя обновлять чужую поездку."""
        url = reverse("trip-detail", kwargs={"pk": another_user_trip.id})
        data = {
            "resort": another_user_trip.resort.id,
            "start_date": another_user_trip.start_date,
            "end_date": another_user_trip.end_date,
            "comment": "Попытка обновить чужую поездку",
            "is_public": True,
        }

        response = authenticated_client.put(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestTripDelete:
    """Тесты DELETE /api/trips/{id}/"""

    def test_delete_own_trip(self, authenticated_client, trip):
        """Пользователь может удалять свою поездку."""
        url = reverse("trip-detail", kwargs={"pk": trip.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Проверяем, что поездка удалена
        from resort.models import Trip

        assert not Trip.objects.filter(id=trip.id).exists()

    def test_delete_another_user_trip(self, authenticated_client, another_user_trip):
        """Нельзя удалять чужую поездку."""
        url = reverse("trip-detail", kwargs={"pk": another_user_trip.id})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Проверяем, что поездка не удалена
        from resort.models import Trip

        assert Trip.objects.filter(id=another_user_trip.id).exists()
