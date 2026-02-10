import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestReadOnlyEndpoints:
    """Проверка, что курорты только для чтения."""

    def test_cannot_create_resort(self, authenticated_client):
        """Нельзя создать курорт через API."""
        url = reverse("resort-list")
        data = {"name": "Новый курорт", "slug": "new", "region": "Тест"}

        response = authenticated_client.post(url, data=data)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_cannot_delete_resort(self, authenticated_client, resort):
        """Нельзя удалить курорт через API."""
        url = reverse("resort-detail", kwargs={"slug": resort.slug})

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
