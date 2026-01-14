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


@pytest.mark.django_db
def test_index_view(client):
    """Тест главной страницы"""
    url = reverse('home')
    response = client.get(url)  # Выполняем GET-запрос к главной странице
    assert response.status_code == 200


@pytest.mark.django_db
def test_resort_detail_view(client, resort):
    """Тест страницы курорта"""
    url = reverse('resort_detail', args=[resort.slug])
    response = client.get(url)  # Выполняем GET-запрос к странице курорта
    assert response.status_code == 200
    assert resort.name in response.content.decode()  # Проверяем, что имя курорта отображается на странице


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