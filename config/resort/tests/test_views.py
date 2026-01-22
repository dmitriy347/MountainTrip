import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from resort.models import Resort, Trip, TripMedia


# 0. Тесты для представления index
def test_index_view(client):
    """Тест главной страницы: статус, шаблон, контекст"""
    url = reverse("home")

    # Выполняем GET-запрос к главной странице
    response = client.get(url)

    # Проверяем, что статус ответа 200
    assert response.status_code == 200

    # Проверяем использование правильного шаблона
    assert "resort/index.html" in [
        t.name for t in response.templates
    ]

    # Проверяем, что заголовок в контексте корректен
    assert (
        response.context["title"] == "Горнолыжные курорты России"
    )


# 1. Тесты для представления ResortDetailView
@pytest.mark.django_db
def test_resort_detail_view_returns_200(client, resort):
    """Тест страницы курорта возвращает 200"""
    url = reverse("resort_detail", kwargs={"resort_slug": resort.slug})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_resort_detail_view_guest_sees_only_counters(
    client, resort, public_trip_another_user, private_trip_another_user
):
    """Гость не видит список поездок на странице курорта, но видит счетчики поездок"""
    url = reverse("resort_detail", kwargs={"resort_slug": resort.slug})
    response = client.get(url)
    assert response.context["trips"] is None  # Гость не видит список поездок
    assert "total_trips_count" in response.context  # Гость видит счетчики
    assert "public_trips_count" in response.context


@pytest.mark.django_db
def test_resort_detail_view_auth_user_sees_correct_trips(
    auth_client,
    resort,
    trip,
    public_trip_another_user_resort,
    private_trip_another_user_resort,
):
    """
    Авторизованный пользователь видит на странице курорта свои поездки,
    публичные поездки других пользователей и счетчики поездок. Не видит приватные поездки других пользователей.
    """
    url = reverse("resort_detail", kwargs={"resort_slug": resort.slug})
    response = auth_client.get(url)
    trips = response.context["trips"]
    assert trips is not None  # Пользователь видит список поездок
    assert trip in trips  # Пользователь видит свою поездку

    # Пользователь видит публичную поездку другого пользователя
    assert (
        public_trip_another_user_resort in trips
    )

    # Пользователь НЕ видит приватную поездку другого пользователя
    assert (
        private_trip_another_user_resort not in trips
    )


@pytest.mark.django_db
def test_resort_detail_view_counters(
    client,
    resort,
    trip,
    public_trip_another_user_resort,
    private_trip_another_user_resort,
):
    """Тест корректности счетчиков поездок на странице курорта"""
    url = reverse("resort_detail", kwargs={"resort_slug": resort.slug})
    response = client.get(url)

    # Общее количество поездок к курорту
    assert (
        response.context["total_trips_count"] == 3
    )

    # Количество публичных поездок к курорту
    assert (
        response.context["public_trips_count"] == 1
    )


# 2. Тесты для представления ResortListView
@pytest.mark.django_db
def test_resort_list_view_returns_resorts(client, resort):
    """Тест страницы списка курортов возвращает 200 и содержит курорты"""
    url = reverse("resort_list")
    response = client.get(url)
    assert response.status_code == 200

    # Проверяем, что курорт присутствует в контексте
    assert (
        resort in response.context["resorts"]
    )


@pytest.mark.django_db
def test_resort_list_view_uses_correct_template(client):
    """Тест использования правильного шаблона для страницы списка курортов"""
    url = reverse("resort_list")
    response = client.get(url)

    # Проверяем использование правильного шаблона
    assert "resort/resort_list.html" in [
        t.name for t in response.templates
    ]


@pytest.mark.django_db
def test_resort_list_view_pagination(client):
    """Тест пагинации на странице списка курортов"""
    # Создаем 8 курортов для проверки пагинации
    for i in range(8):
        Resort.objects.create(
            name=f"Resort {i}", region="Test Region", description="Test description"
        )

    url = reverse("resort_list")

    # Запрашиваем первую страницу
    response_page_1 = client.get(
        url
    )
    assert response_page_1.status_code == 200

    # Проверяем, что на первой странице отображается 5 курортов
    assert (
        len(response_page_1.context["resorts"]) == 6
    )

    # Запрашиваем вторую страницу
    response_page_2 = client.get(url + "?page=2")
    assert response_page_2.status_code == 200

    # Проверяем, что на второй странице отображается оставшиеся 3 курорта
    assert (
        len(response_page_2.context["resorts"]) == 2
    )


# 3. Тесты для представления TripDetailView
@pytest.mark.django_db
def test_trip_detail_view_requires_login(client, trip):
    """Тест доступа к странице детали поездки (требуется авторизация)"""
    url = reverse("trip_detail", kwargs={"trip_id": trip.id})
    response = client.get(url)
    assert response.status_code == 302  # Ожидаем перенаправление на страницу логина

    # Проверяем, что перенаправление ведет на страницу логина
    assert (
        "/sign-in/" in response.url
    )


@pytest.mark.django_db
def test_trip_detail_view_owner_can_access(auth_client, trip):
    """Владелец может открыть свою поездку"""
    url = reverse("trip_detail", kwargs={"trip_id": trip.id})
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_trip_detail_view_public_trip_visible(auth_client, public_trip_another_user):
    """Авторизованный пользователь может видеть публичную поездку другого пользователя"""
    url = reverse("trip_detail", kwargs={"trip_id": public_trip_another_user.id})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.context["trip"] == public_trip_another_user


@pytest.mark.django_db
def test_trip_detail_view_private_trip_visible(auth_client, private_trip_another_user):
    """Авторизованный пользователь НЕ может видеть приватную поездку другого пользователя"""
    url = reverse("trip_detail", kwargs={"trip_id": private_trip_another_user.id})
    response = auth_client.get(url)

    # Ожидаем 404, т.к. поездка приватная и не принадлежит пользователю
    assert (
        response.status_code == 404
    )


@pytest.mark.django_db
def test_trip_detail_view_media_in_context(auth_client, trip, trip_media):
    """Тест наличия медиафайлов в контексте страницы детали поездки"""
    url = reverse("trip_detail", kwargs={"trip_id": trip.id})
    response = auth_client.get(url)
    media = response.context["media_list"]

    # Проверяем, что медиафайл присутствует в контексте
    assert trip_media in media


@pytest.mark.django_db
def test_trip_detail_view_has_title(auth_client, trip):
    """Тест наличия заголовка на странице детали поездки"""
    url = reverse("trip_detail", kwargs={"trip_id": trip.id})
    response = auth_client.get(url)
    assert "title" in response.context


# 4. Тесты для представления TripListView
def test_trip_list_view_requires_login(client):
    """Тест доступа к странице списка поездок (требуется авторизация)"""
    url = reverse("trip_list")
    response = client.get(url)
    assert response.status_code == 302  # Ожидаем перенаправление на страницу логина

    # Проверяем, что перенаправление ведет на страницу логина
    assert (
        "/sign-in/" in response.url
    )


@pytest.mark.django_db
def test_trip_list_view_authenticated_user(auth_client):
    """Тест доступа к странице списка поездок для авторизованного пользователя"""
    url = reverse("trip_list")
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_trip_list_view_shows_only_user_trips(
    auth_client, trip, public_trip_another_user, private_trip_another_user
):
    """Пользователь должен видеть ТОЛЬКО свои поездки в списке поездок (OwnerQuerySetMixin)"""
    url = reverse("trip_list")
    response = auth_client.get(url)
    trips = response.context["trips"]
    assert trip in trips  # Пользователь видит свою поездку

    # Пользователь НЕ видит публичную поездку другого пользователя
    assert (
        public_trip_another_user not in trips
    )

    # Пользователь НЕ видит приватную поездку другого пользователя
    assert (
        private_trip_another_user not in trips
    )


@pytest.mark.django_db
def test_trip_list_view_has_title(auth_client):
    """Тест наличия заголовка на странице списка поездок"""
    url = reverse("trip_list")
    response = auth_client.get(url)

    # Проверяем, что заголовок страницы корректен
    assert (
        response.context["title"] == "Мои поездки"
    )


# 5. Тесты для представления TripCreateView
def test_trip_create_requires_login(client):
    """Тест доступа к странице создания поездки (требуется авторизация)"""
    url = reverse("trip_create")
    response = client.get(url)
    assert response.status_code == 302  # Ожидаем перенаправление на страницу логина
    assert "/sign-in/" in response.url  # Проверяем, что перенаправление ведет на страницу логина


@pytest.mark.django_db
def test_trip_create_view(auth_client):
    """Тест страницы создания поездки для авторизованного пользователя"""
    url = reverse("trip_create")
    response = auth_client.get(url)  # Выполняем GET-запрос к странице создания поездки
    assert response.status_code == 200
    assert (
        "form" in response.context
    )  # Проверяем, что авторизованный пользователь видит форму создания поездки


@pytest.mark.django_db
def test_trip_create_view_assigns_user(auth_client, user, resort):
    """Тест успешного редиректа и присвоения пользователя при создании поездки"""
    url = reverse("trip_create")
    form_data = {
        "resort": resort.id,
        "start_date": "2024-01-01",
        "end_date": "2024-01-05",
        "is_public": True,
    }
    response = auth_client.post(
        url, data=form_data
    )  # Отправляем POST-запрос с данными формы
    assert response.status_code == 302  # Ожидаем редирект после успешного создания
    trip = Trip.objects.get()  # Получаем созданную поездку
    assert trip.user == user  # Проверяем, что пользователь присвоен корректно


# 6. Тесты для представления TripUpdateView
@pytest.mark.django_db
def test_trip_update_view_requires_login(client, trip):
    """Тест доступа к странице редактирования поездки (требуется авторизация)"""
    url = reverse("trip_edit", kwargs={"trip_id": trip.id})
    response = client.get(url)  # Выполняем GET-запрос к странице редактирования поездки
    assert response.status_code == 302  # Ожидаем перенаправление на страницу логина

    # Проверяем, что перенаправление ведет на страницу логина
    assert (
        "/sign-in/" in response.url
    )


@pytest.mark.django_db
def test_trip_update_view_not_owner_cannot_access(client, another_user, trip):
    """Пользователь не-владелец не может редактировать чужую поездку"""
    url = reverse("trip_edit", kwargs={"trip_id": trip.id})
    client.force_login(another_user)  # Логинимся как другой пользователь
    response = client.get(url)

    # Ожидаем 404, так как пользователь не владелец поездки
    assert (
        response.status_code == 404
    )


@pytest.mark.django_db
def test_trip_update_view_owner_can_open(auth_client, trip):
    """Владелец может открыть страницу редактирования своей поездки"""
    url = reverse("trip_edit", kwargs={"trip_id": trip.id})
    response = auth_client.get(
        url
    )
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_trip_update_view_owner_can_save(auth_client, trip):
    """Владелец может успешно сохранить изменения поездки"""
    url = reverse("trip_edit", kwargs={"trip_id": trip.id})
    form_data = {
        "resort": trip.resort.id,
        "start_date": "2023-12-01",
        "end_date": "2023-12-10",
        "is_public": True,
    }

    # Отправляем POST-запрос с измененными данными
    response = auth_client.post(
        url, data=form_data
    )
    trip.refresh_from_db()  # Обновляем объект поездки из базы данных
    assert response.status_code == 302  # Ожидаем редирект после успешного сохранения
    assert trip.is_public is True  # Проверяем, что изменения сохранены
    messages = list(get_messages(response.wsgi_request))  # Получаем сообщения
    assert len(messages) == 1


# 7. Тесты для представления TripDeleteView
@pytest.mark.django_db
def test_trip_delete_view_requires_login(client, trip):
    """Тест доступа к странице удаления поездки (требуется авторизация)"""
    url = reverse("trip_delete", kwargs={"trip_id": trip.id})
    response = client.post(url)
    assert response.status_code == 302
    assert (
        "/sign-in/" in response.url
    )

    # Проверяем, что поездка не была удалена
    assert Trip.objects.filter(
        id=trip.id
    ).exists()


@pytest.mark.django_db
def test_trip_delete_view_not_owner_cannot_access(client, another_user, trip):
    """Пользователь не-владелец не может удалить чужую поездку"""
    url = reverse("trip_delete", kwargs={"trip_id": trip.id})
    client.force_login(another_user)  # Логинимся как другой пользователь
    response = client.post(url)  # Выполняем POST-запрос к странице удаления поездки

    # Ожидаем 404, так как пользователь не владелец поездки
    assert (
        response.status_code == 404
    )


@pytest.mark.django_db
def test_trip_delete_view_owner_can_delete(auth_client, trip):
    """Владелец может успешно удалить свою поездку"""
    url = reverse("trip_delete", kwargs={"trip_id": trip.id})
    response = auth_client.post(
        url
    )
    assert response.status_code == 302

    # Проверяем, что поездка была удалена
    assert not Trip.objects.filter(
        id=trip.id
    ).exists()
    messages = list(get_messages(response.wsgi_request))

    # Проверяем, что появилось сообщение об успешном удалении
    assert len(messages) == 1


# 8. Тесты для представления TripMediaAddView
@pytest.mark.django_db
def test_trip_media_add_view_requires_login(client, trip):
    """Тест доступа к странице добавления медиафайла (требуется авторизация)"""
    url = reverse("trip_media_add", kwargs={"trip_id": trip.id})
    response = client.post(
        url
    )
    assert response.status_code == 302
    assert (
        "/sign-in/" in response.url
    )


@pytest.mark.django_db
def test_trip_media_add_view_not_owner_cannot_access(
    client, another_user, trip, image_file
):
    """Пользователь не-владелец не может добавить медиафайл к чужой поездке"""
    url = reverse("trip_media_add", kwargs={"trip_id": trip.id})
    client.force_login(another_user)  # Логинимся как другой пользователь
    form_data = {
        "image": image_file,
    }
    response = client.post(url, data=form_data)  # Отправляем POST-запрос с медиафайлом

    # Ожидаем 404, так как пользователь не владелец поездки
    assert (
        response.status_code == 404
    )


@pytest.mark.django_db
def test_trip_media_add_view_owner_can_save(auth_client, trip, image_file):
    """Владелец может успешно добавить медиафайл к своей поездке"""
    url = reverse("trip_media_add", kwargs={"trip_id": trip.id})
    form_data = {
        "image": image_file,
    }
    response = auth_client.post(
        url, data=form_data
    )
    assert (
        response.status_code == 302
    )
    media = TripMedia.objects.get(trip=trip)  # Получаем добавленный медиафайл
    assert media.image.name  # Проверяем, что медиафайл был сохранен
    messages = list(get_messages(response.wsgi_request))  # Получаем сообщения
    assert len(messages) == 1

    # Проверяем, что появилось сообщение об успешном добавлении
    assert (
        messages[0].message == "Фото успешно добавлено."
    )


# 9. Тесты для представления TripMediaDeleteView
@pytest.mark.django_db
def test_trip_media_delete_view_requires_login(client, trip_media):
    """Тест доступа к странице удаления медиафайла (требуется авторизация)"""
    url = reverse("trip_media_delete", kwargs={"media_id": trip_media.id})
    response = client.post(url)
    assert response.status_code == 302
    assert (
        "/sign-in/" in response.url
    )

    # Проверяем, что медиафайл не был удален
    assert TripMedia.objects.filter(
        id=trip_media.id
    ).exists()


@pytest.mark.django_db
def test_trip_media_delete_view_not_owner_cannot_access(
    client, another_user, trip_media
):
    """Пользователь не-владелец не может удалить чужой медиафайл"""
    url = reverse("trip_media_delete", kwargs={"media_id": trip_media.id})
    client.force_login(another_user)  # Логинимся как другой пользователь
    response = client.post(url)

    # Ожидаем 404, так как пользователь не владелец медиафайла
    assert (
        response.status_code == 404
    )

    # Проверяем, что медиафайл не был удален
    assert TripMedia.objects.filter(
        id=trip_media.id
    ).exists()


@pytest.mark.django_db
def test_trip_media_delete_view_owner_can_delete(auth_client, trip_media):
    """Владелец может успешно удалить свой медиафайл"""
    url = reverse("trip_media_delete", kwargs={"media_id": trip_media.id})
    response = auth_client.post(
        url
    )
    assert response.status_code == 302

    # Проверяем, что медиафайл был удален
    assert not TripMedia.objects.filter(
        id=trip_media.id
    ).exists()
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].message == "Фото удалено."
