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
