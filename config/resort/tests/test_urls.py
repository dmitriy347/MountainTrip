import pytest
from django.urls import reverse, resolve

from resort import views


@pytest.mark.django_db
def test_home_url():
    """Тестирование URL главной страницы"""
    url = reverse('home')
    assert url == '/'   # Проверяем, что URL для имени 'home' равен '/'
    match = resolve(url)
    assert match.func == views.index  # Проверяем, что URL разрешается в правильное представление


@pytest.mark.django_db
def test_resort_detail_url(resort):
    """Тестирование URL страницы курорта"""
    url = reverse('resort_detail', kwargs={'resort_slug': resort.slug})
    assert url == f'/resort/{resort.slug}'  # Проверяем, что URL для имени 'resort_detail' корректен
    match = resolve(url)
    assert match.func.view_class == views.ResortDetailView  # Проверяем, что URL разрешается в правильное представление


@pytest.mark.django_db
def test_resort_list_urls():
    """Тестирование URL для списка курортов и поездок"""
    url = reverse('resort_list')
    assert url == '/resorts/'  # Проверяем URL для списка курортов
    match = resolve(url)
    assert match.func.view_class == views.ResortListView  # Проверяем представление для


@pytest.mark.django_db
def test_trip_list_url():
    """Тестирование URL для списка поездок"""
    url = reverse('trip_list')
    assert url == '/trips/'  # Проверяем URL для списка поездок
    match = resolve(url)
    assert match.func.view_class == views.TripListView  # Проверяем представление для списка поездок


@pytest.mark.django_db
def test_trip_urls_reverse_and_resolve():
    assert reverse('trip_list') == '/trips/'
    assert reverse('trip_create') == '/trips/create'
    assert reverse('trip_detail', kwargs={'trip_id': 1}) == '/trip/1'
    assert reverse('trip_edit', kwargs={'trip_id': 1}) == '/trips/1/edit'
    assert reverse('trip_delete', kwargs={'trip_id': 1}) == '/trips/1/delete'
    assert reverse('trip_media_add', kwargs={'trip_id': 1}) == '/trips/1/media/add'
    assert reverse('trip_media_delete', kwargs={'media_id': 1}) == '/media/1/delete/'

    assert resolve('/trip/1').func.view_class is views.TripDetailView
    assert resolve('/trips/1/edit').func.view_class is views.TripUpdateView
    assert resolve('/trips/1/media/add').func.view_class is views.TripMediaAddView
    assert resolve('/media/1/delete/').func.view_class is views.TripMediaDeleteView