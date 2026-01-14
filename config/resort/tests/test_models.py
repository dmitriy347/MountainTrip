# Тесты для моделей Resort, Trip, TripMedia.

import pytest
from django.urls import reverse
from django.utils.text import slugify

from resort.models import Resort, Trip, TripMedia

@pytest.mark.django_db
def test_resort_str():
    """__str__ должен возвращать название курорта."""
    resort = Resort.objects.create(name="Test Resort", region="Test Region")
    assert str(resort) == "Test Resort"


@pytest.mark.django_db
def test_resort_slug_created(db):
    """Slug должен автоматически создаваться при сохранении курорта."""
    resort = Resort.objects.create(name="Test Resort", region="Test Region")
    assert resort.slug == slugify("Test Resort")


@pytest.mark.django_db
def test_resort_get_absolute_url():
    """get_absolute_url должен возвращать корректный URL"""
    resort = Resort.objects.create(name="URL Resort", region="URL Region")
    url = resort.get_absolute_url()

    assert resort.slug in url