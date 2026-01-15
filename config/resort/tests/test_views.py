# Тесты для основных view:
# Для config/resort/views.py ориентировочно 25–30 тестов. Ниже — краткая разбивка по представлениям (примерное число тестов на каждый):
#
# - index — 1 (рендер, статус, заголовок)
# - ResortDetailView — 4 (контекстный заголовок, кеширование/счётчики, гость не видит поездки, авторизованный видит свои и публичные)
# - ResortListView — 2 (кеширование списка, пагинация/шаблон)
# - TripDetailView — 3 (login required, видимость/фильтрация записей, media в контексте)
# - TripListView — 2 (login required, только поездки текущего пользователя + заголовок)
# - TripCreateView — 3 (login required, при создании присваивается user, сообщение и редирект)
# - TripUpdateView — 3 (login + owner ограничение, успешное сохранение и сообщение, запрещён доступ не-владельцу)
# - TripDeleteView — 3 (login + owner, удаление и сообщение, редирект на список)
# - TripMediaAddView — 3 (login, добавление только к своей поездке, сообщение/редирект)
# - TripMediaDeleteView — 3 (owner только, сообщение и редирект к детали поездки, опционально сигнал удаления файла)
# - page_not_found — 1 (возвращает 404)

import pytest
from django.urls import reverse
from resort.models import Resort


# Тесты для представления ResortDetailView
@pytest.mark.django_db
def test_resort_detail_view_returns_200(client, resort):
    """Тест страницы курорта возвращает 200"""
    url = reverse('resort_detail', kwargs={'resort_slug': resort.slug})
    response = client.get(url)          # Выполняем GET-запрос к странице курорта
    assert response.status_code == 200


@pytest.mark.django_db
def test_resort_detail_view_guest_sees_only_counters(
        client,
        resort,
        public_trip_another_user,
        private_trip_another_user
):
    """Гость не видит список поездок на странице курорта, но видит счетчики поездок"""
    url = reverse('resort_detail', kwargs={'resort_slug': resort.slug})
    response = client.get(url)                      # Выполняем GET-запрос к странице курорта
    assert response.context['trips'] is None        # Гость не видит список поездок
    assert 'total_trips_count' in response.context  # Гость видит счетчики
    assert 'public_trips_count' in response.context


@pytest.mark.django_db
def test_resort_detail_view_auth_user_sees_correct_trips(
        auth_client,
        resort,
        trip,
        public_trip_another_user_resort,
        private_trip_another_user_resort
):
    """
    Авторизованный пользователь видит на странице курорта свои поездки,
    публичные поездки других пользователей и счетчики поездок. Не видит приватные поездки других пользователей.
    """
    url = reverse('resort_detail', kwargs={'resort_slug': resort.slug})
    response = auth_client.get(url)                      # Выполняем GET-запрос к странице курорта
    trips = response.context['trips']
    assert trips is not None                             # Пользователь видит список поездок
    assert trip in trips                                 # Пользователь видит свою поездку
    assert public_trip_another_user_resort in trips      # Пользователь видит публичную поездку другого пользователя
    assert private_trip_another_user_resort not in trips # Пользователь НЕ видит приватную поездку другого пользователя


@pytest.mark.django_db
def test_resort_detail_view_counters(
        client,
        resort,
        trip,
        public_trip_another_user_resort,
        private_trip_another_user_resort
):
    """Тест корректности счетчиков поездок на странице курорта"""
    url = reverse('resort_detail', kwargs={'resort_slug': resort.slug})
    response = client.get(url)                          # Выполняем GET-запрос к странице курорта
    assert response.context['total_trips_count'] == 3   # Общее количество поездок к курорту
    assert response.context['public_trips_count'] == 1  # Количество публичных поездок к курорту


# Тесты для представления ResortListView
@pytest.mark.django_db
def test_resort_list_view_returns_resorts(client, resort):
    """Тест страницы списка курортов возвращает 200 и содержит курорты"""
    url = reverse('resort_list')
    response = client.get(url)                    # Выполняем GET-запрос к странице списка курортов
    assert response.status_code == 200
    assert resort in response.context['resorts']  # Проверяем, что курорт присутствует в контексте


@pytest.mark.django_db
def test_resort_list_view_uses_correct_template(client):
    """Тест использования правильного шаблона для страницы списка курортов"""
    url = reverse('resort_list')
    response = client.get(url)                                          # Выполняем GET-запрос к странице списка курортов
    assert 'resort/resort_list.html' in [t.name for t in response.templates]  # Проверяем использование правильного шаблона


@pytest.mark.django_db
def test_resort_list_view_pagination(client):
    """Тест пагинации на странице списка курортов"""
    # Создаем 8 курортов для проверки пагинации
    for i in range(8):
        Resort.objects.create(name=f'Resort {i}', region='Test Region', description='Test description')

    url = reverse('resort_list')
    response_page_1 = client.get(url)                    # Выполняем GET-запрос к первой странице списка курортов
    assert response_page_1.status_code == 200
    assert len(response_page_1.context['resorts']) == 5  # Проверяем, что на первой странице отображается 5 курортов

    response_page_2 = client.get(url + '?page=2')        # Запрашиваем вторую страницу
    assert response_page_2.status_code == 200
    assert len(response_page_2.context['resorts']) == 3  # Проверяем, что на второй странице отображается оставшиеся 4 курорта


# Тесты для представления TripDetailView
@pytest.mark.django_db
def test_trip_detail_view_requires_login(client, trip):
    """Тест доступа к странице детали поездки (требуется авторизация)"""
    url = reverse('trip_detail', kwargs={'trip_id': trip.id})
    response = client.get(url)                  # Выполняем GET-запрос к странице детали поездки
    assert response.status_code == 302          # Ожидаем перенаправление на страницу логина
    assert '/sign-in/' in response.url          # Проверяем, что перенаправление ведет на страницу логина





# Тесты для представления TripListView
def test_trip_list_view_requires_login(client):
    """Тест доступа к странице списка поездок (требуется авторизация)"""
    url = reverse('trip_list')
    response = client.get(url)                  # Выполняем GET-запрос к странице списка поездок
    assert response.status_code == 302          # Ожидаем перенаправление на страницу логина
    assert '/sign-in/' in response.url          # Проверяем, что перенаправление ведет на страницу логина


@pytest.mark.django_db
def test_trip_list_view_authenticated_user(auth_client):
    """Тест доступа к странице списка поездок для авторизованного пользователя"""
    url = reverse('trip_list')
    response = auth_client.get(url)             # Выполняем GET-запрос к странице списка поездок
    assert response.status_code == 200


@pytest.mark.django_db
def test_trip_list_view_shows_only_user_trips(
        auth_client,
        trip,
        public_trip_another_user,
        private_trip_another_user
):
    """Пользователь должен видеть ТОЛЬКО свои поездки в списке поездок (OwnerQuerySetMixin)"""
    url = reverse('trip_list')
    response = auth_client.get(url)             # Выполняем GET-запрос к странице списка поездок
    trips = response.context['trips']
    assert trip in trips                             # Пользователь видит свою поездку
    assert public_trip_another_user not in trips     # Пользователь НЕ видит публичную поездку другого пользователя
    assert private_trip_another_user not in trips    # Пользователь НЕ видит приватную поездку другого пользователя


@pytest.mark.django_db
def test_trip_list_view_has_title(auth_client):
    """Тест наличия заголовка на странице списка поездок"""
    url = reverse('trip_list')
    response = auth_client.get(url)                    # Выполняем GET-запрос к странице списка поездок
    assert response.context['title'] == 'Мои поездки'  # Проверяем, что заголовок страницы корректен






# Тесты для представления index
@pytest.mark.django_db
def test_index_view(client):
    """Тест главной страницы"""
    url = reverse('home')
    response = client.get(url)  # Выполняем GET-запрос к главной странице
    assert response.status_code == 200


@pytest.mark.django_db
def test_trip_create_requires_login(client):
    """Тест доступа к странице создания поездки (требуется авторизация)"""
    url = reverse('trip_create')
    response = client.get(url)  # Выполняем GET-запрос к странице создания поездки
    assert response.status_code == 302  # Ожидаем перенаправление на


@pytest.mark.django_db
def test_trip_create_view(auth_client):
    """Тест страницы создания поездки для авторизованного пользователя"""
    url = reverse('trip_create')
    response = auth_client.get(url)  # Выполняем GET-запрос к странице создания поездки
    assert response.status_code == 200