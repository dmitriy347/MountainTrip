# Тесты для моделей Resort, Trip, TripMedia.

import pytest
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Тесты для модели Resort
@pytest.mark.django_db
def test_resort_str(resort):
    """__str__ должен возвращать название курорта."""
    assert str(resort) == "Test Resort"


@pytest.mark.django_db
def test_resort_slug_created(resort):
    """Slug должен автоматически создаваться при сохранении курорта."""
    assert resort.slug == slugify(resort.name)


@pytest.mark.django_db
def test_resort_get_absolute_url(resort):
    """get_absolute_url должен возвращать корректный URL"""
    url = resort.get_absolute_url()
    assert resort.slug in url


# Тесты для модели Trip
@pytest.mark.django_db
def test_trip_str(trip):
    """__str__ должен возвращать строку с именем пользователя и названием курорта."""
    assert str(trip) == f"{trip.user.username} - {trip.resort.name}"


@pytest.mark.django_db
def test_trip_clean_valid_dates(trip):
    """clean не должен вызывать ошибку для валидных дат."""
    try:
        trip.clean()
    except ValidationError:
        pytest.fail("Возникла ValidationError для валидных дат.")


@pytest.mark.django_db
def test_trip_clean_invalid_dates(trip_invalid):
    """clean должен вызывать ValidationError, если дата начала позже даты окончания."""
    with pytest.raises(ValidationError):
        trip_invalid.clean()


@pytest.mark.django_db
def test_trip_get_absolute_url(trip):
    """get_absolute_url должен возвращать корректный URL для поездки."""
    url = trip.get_absolute_url()
    assert str(trip.id) in url


# Тесты для модели TripMedia
@pytest.mark.django_db
def test_tripmedia_str(trip_media):
    """__str__ должен возвращать строку с ID поездки."""
    assert str(trip_media) == f'Media for trip {trip_media.trip.id}'


@pytest.mark.django_db
def test_tripmedia_get_absolute_url(trip_media):
    """get_absolute_url должен возвращать корректный URL для медиа поездки."""
    url = trip_media.trip.get_absolute_url()
    assert str(trip_media.trip.id) in url