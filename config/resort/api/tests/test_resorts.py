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


@pytest.mark.django_db
class TestResortDetail:
    """Тесты GET /api/resorts/{slug}/"""

    def test_get_resort_by_slug(self, api_client, resort):
        """Получение курорта по slug."""
        url = reverse("resort-detail", kwargs={"slug": resort.slug})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == resort.id
        assert response.data["name"] == resort.name
        assert response.data["slug"] == resort.slug
        assert response.data["region"] == resort.region
        assert response.data["description"] == resort.description

    def test_get_resort_not_found(self, api_client):
        """Курорт не найден."""
        url = reverse("resort-detail", kwargs={"slug": "non-existent"})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestResortTripsEndpoint:
    """Тесты GET /api/resorts/{slug}/trips/ (вложенный эндпоинт)"""

    # def test_resort_trips_as_guest(self, api_client, resort, trip, private_trip):
    #     """Гость видит только публичные поездки курорта."""
    #     url = reverse("resort-trips", kwargs={"slug": resort.slug})
    #
    #     response = api_client.get(url)
    #
    #     assert response.status_code == status.HTTP_200_OK
    #     assert len(response.data) == 1
    #     assert response.data[0]["id"] == trip.id

    def test_resort_trips_empty(self, api_client, resort):
        """Курорт без поездок."""
        url = reverse("resort-trips", kwargs={"slug": resort.slug})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_resort_trips_not_found(self, api_client):
        """Несуществующий курорт."""
        url = reverse("resort-trips", kwargs={"slug": "non-existent"})

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
