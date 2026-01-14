# Тесты для моделей Resort, Trip, TripMedia.

import pytest
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


# @pytest.mark.django_db
# def test_trip_str(trip):
#     """__str__ должен возвращать строку с именем пользователя и названием курорта."""
#     assert str(trip) == f"{trip.user.username} - {trip.resort.name}"


# @pytest.mark.django_db
# def test_trip_clean_
