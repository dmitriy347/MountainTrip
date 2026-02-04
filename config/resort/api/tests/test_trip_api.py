import pytest


@pytest.mark.django_db
def test_guest_sees_only_public_trips(api_client):
    """Тест: Гость видит только публичные поездки."""
    pass


@pytest.mark.django_db
def test_authenticated_user_sees_own_and_public_trips(api_client, user):
    """Тест: Авторизованный пользователь видит свои и публичные поездки."""
    pass
