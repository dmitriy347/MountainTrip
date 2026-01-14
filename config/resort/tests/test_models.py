# Тесты для моделей Resort, Trip, TripMedia.

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.text import slugify

from resort.models import Resort, Trip, TripMedia


@pytest.mark.django_db
def test_resort_str(resort):
    """__str__ должен возвращать название курорта."""
    assert str(resort) == "Test Resort"


@pytest.mark.django_db
def test_resort_slug_created(resort):
    """Slug должен автоматически создаваться при сохранении курорта."""
    assert resort.slug == slugify(resort.name)
    assert 'test' in resort.slug or 'resort' in resort.slug # нужна ли эта проверка?


@pytest.mark.django_db
def test_resort_get_absolute_url(resort):
    """get_absolute_url должен возвращать корректный URL"""
    url = resort.get_absolute_url()
    assert resort.slug in url


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


def test_trip_get_absolute_url(trip):
    """get_absolute_url должен возвращать корректный URL для поездки."""
    url = trip.get_absolute_url()
    assert str(trip.id) in url