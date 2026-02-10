import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestResortFilters:
    """Тесты для фильтрации курортов."""

    def test_filter_by_region(self, api_client, resort, another_resort):
        """Фильтр по региону (частичное совпадение)."""
        url = reverse("resort-list")

        response = api_client.get(url, {"region": "Краснода"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == resort.id

    def test_search_resorts(self, api_client, resort, another_resort):
        """Поиск по нескольким полям."""
        url = reverse("resort-list")

        response = api_client.get(url, {"search": "Шерегеш"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == another_resort.id

    def test_ordering_resorts_by_name(self, api_client, resort, another_resort):
        """Сортировка по названию курорта."""
        url = reverse("resort-list")

        response = api_client.get(url, {"ordering": "name"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        assert response.data["results"][0]["name"] == "Роза Хутор"
        assert response.data["results"][1]["name"] == "Шерегеш"

    def test_ordering_resorts_by_region_desc(self, api_client, resort, another_resort):
        """Сортировка по региону (обратный порядок)."""
        url = reverse("resort-list")

        response = api_client.get(url, {"ordering": "-region"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2
        assert response.data["results"][0]["region"] == "Краснодарский край"
        assert response.data["results"][1]["region"] == "Кемеровская область"


@pytest.mark.django_db
class TestTripFilters:
    """Тесты для фильтрации поездок."""

    def test_filter_by_is_public(self, api_client, trip, private_trip):
        """Фильтр по публичности поездки."""
        url = reverse("trip-list")

        response = api_client.get(url, {"is_public": True})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == trip.id

    def test_filter_by_resort(self, api_client, resort, another_resort, trip, user):
        """Фильтр по курорту (ID)."""
        from resort.models import Trip

        trip2 = Trip.objects.create(
            user=user,
            resort=another_resort,
            start_date="2024-05-01",
            end_date="2024-05-07",
            is_public=True,
        )

        url = reverse("trip-list")

        response = api_client.get(url, {"resort_id": resort.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert trip2 not in response.data["results"]
        assert response.data["results"][0]["resort"]["id"] == resort.id

    def test_filter_by_resort_region(self, api_client, resort, trip):
        """Фильтр по региону курорта."""
        url = reverse("trip-list")

        response = api_client.get(url, {"resort_region": "Красно"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == trip.id

    def test_filter_by_start_date_from(self, api_client, resort, user):
        """Фильтр по дате начала поездки (от)."""
        from resort.models import Trip

        trip_old = Trip.objects.create(
            user=user,
            resort=resort,
            start_date="2024-01-01",
            end_date="2024-01-07",
            is_public=True,
        )
        trip_new = Trip.objects.create(
            user=user,
            resort=resort,
            start_date="2024-03-01",
            end_date="2024-03-07",
            is_public=True,
        )
        url = reverse("trip-list")

        # Поездки начиная с 2024-02-01
        response = api_client.get(url, {"start_date_from": "2024-02-01"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert trip_old not in response.data["results"]
        assert response.data["results"][0]["id"] == trip_new.id

    def test_filter_by_date_range(self, api_client, resort, user):
        """Фильтр по диапазону дат поезки."""
        from resort.models import Trip

        trip1 = Trip.objects.create(
            user=user,
            resort=resort,
            start_date="2024-01-15",
            end_date="2024-01-20",
            is_public=True,
        )
        trip2 = Trip.objects.create(
            user=user,
            resort=resort,
            start_date="2024-02-15",
            end_date="2024-02-20",
            is_public=True,
        )
        trip3 = Trip.objects.create(
            user=user,
            resort=resort,
            start_date="2024-03-15",
            end_date="2024-03-20",
            is_public=True,
        )

        url = reverse("trip-list")

        # Диапазон с 2024-02-01 по 2024-02-28
        response = api_client.get(
            url, {"start_date_from": "2024-02-01", "start_date_to": "2024-02-28"}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert trip1 and trip3 not in response.data["results"]
        assert response.data["results"][0]["id"] == trip2.id

    def test_search_trips(self, api_client, resort, trip, another_user_trip):
        """Поиск поездок по комментарию."""
        url = reverse("trip-list")

        response = api_client.get(url, {"search": "Отличная"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == trip.id

    def test_ordering_trips_by_start_date(self, api_client, resort, user):
        """Сортировка поездок по дате начала."""
        from resort.models import Trip

        trip1 = Trip.objects.create(
            user=user,
            resort=resort,
            start_date="2024-03-01",
            end_date="2024-03-07",
            is_public=True,
        )
        trip2 = Trip.objects.create(
            user=user,
            resort=resort,
            start_date="2024-01-01",
            end_date="2024-01-07",
            is_public=True,
        )

        url = reverse("trip-list")

        response = api_client.get(url, {"ordering": "start_date"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0]["id"] == trip2.id
        assert response.data["results"][1]["id"] == trip1.id
