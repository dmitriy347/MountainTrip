import pytest
from django.urls import reverse, resolve

from resort import views


def test_home_url_resolves():
    """Тестирование URL главной страницы"""
    url = reverse('home')
    match = resolve(url)
    assert match.func is views.index  # Проверяем, что URL разрешается в правильное представление


@pytest.mark.django_db
def test_resort_detail_url_resolves(resort):
    """Тестирование URL страницы курорта"""
    url = reverse('resort_detail', kwargs={'resort_slug': resort.slug})
    match = resolve(url)
    assert match.func.view_class is views.ResortDetailView


def test_resort_list_url_resolves():
    """Тестирование URL для списка курортов"""
    url = reverse('resort_list')
    match = resolve(url)
    assert match.func.view_class is views.ResortListView


@pytest.mark.django_db
def test_trip_detail_url_resolves(trip):
    """Тестирование URL страницы поездки"""
    url = reverse('trip_detail', kwargs={'trip_id': trip.id})
    match = resolve(url)
    assert match.func.view_class is views.TripDetailView


def test_trip_list_url_resolves():
    """Тестирование URL для списка поездок"""
    url = reverse('trip_list')
    match = resolve(url)
    assert match.func.view_class is views.TripListView


def test_trip_create_url_resolves():
    """Тестирование URL для создания поездки"""
    url = reverse('trip_create')
    match = resolve(url)
    assert match.func.view_class is views.TripCreateView


@pytest.mark.django_db
def test_trip_edit_url_resolves(trip):
    """Тестирование URL для редактирования поездки"""
    url = reverse('trip_edit', kwargs={'trip_id': trip.id})
    match = resolve(url)
    assert match.func.view_class is views.TripUpdateView


@pytest.mark.django_db
def test_trip_delete_url_resolves(trip):
    """Тестирование URL для удаления поездки"""
    url = reverse('trip_delete', kwargs={'trip_id': trip.id})
    match = resolve(url)
    assert match.func.view_class is views.TripDeleteView


@pytest.mark.django_db
def test_trip_media_add_url_resolves(trip):
    """Тестирование URL для добавления медиафайла к поездке"""
    url = reverse('trip_media_add', kwargs={'trip_id': trip.id})
    match = resolve(url)
    assert match.func.view_class is views.TripMediaAddView


@pytest.mark.django_db
def test_trip_media_delete_url_resolves(trip_media):
    """Тестирование URL для удаления медиафайла поездки"""
    url = reverse('trip_media_delete', kwargs={'media_id': trip_media.id})
    match = resolve(url)
    assert match.func.view_class is views.TripMediaDeleteView


