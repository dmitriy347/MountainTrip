import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


# 0. Тесты для представления UserLoginView
@pytest.mark.django_db
def test_user_login_view_test_page_accessible(client, social_app):
    """Страница логина доступна для анонимного пользователя."""
    url = reverse('users:login')
    response = client.get(url)
    assert response.status_code == 200                                  # Страница доступна
    assert 'users/login.html' in [t.name for t in response.templates]   # Используется правильный шаблон


@pytest.mark.django_db
def test_user_login_view_successful_login(client, user):
    """Пользователь может успешно войти в систему с правильными учетными данными."""
    url = reverse('users:login')
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    response = client.post(url, data)
    assert response.status_code == 302              # Перенаправление после успешного входа
    assert response.url == reverse('trip_list')     # Перенаправление на страницу списка поездок (LOGIN_REDIRECT_URL)

    # Проверка наличия сообщения об успешном входе
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Вы успешно вошли в систему'


@pytest.mark.django_db
def test_user_login_view_wrong_password(client, user, social_app):
    """Пользователь не может войти с неправильным паролем."""
    url = reverse('users:login')
    data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }
    response = client.post(url, data)
    assert response.status_code == 200          # Страница перезагружается с ошибкой
    assert 'users/login.html' in [t.name for t in response.templates]
    assert response.context['form'].errors      # Форма содержит ошибки


@pytest.mark.django_db
def test_user_login_view_wrong_username(client, user, social_app):
    """Пользователь не может войти с неправильным именем пользователя."""
    url = reverse('users:login')
    data = {
        'username': 'wronguser',
        'password': 'testpass123'
    }
    response = client.post(url, data)
    assert response.status_code == 200          # Страница перезагружается с ошиб
    assert response.context['form'].errors



# 1. Тесты для представления UserLogoutView
@pytest.mark.django_db
def test_user_logout_view_successful_logout(auth_client):
    """Авторизованный пользователь может успешно выйти из системы."""
    url = reverse('users:logout')
    response = auth_client.post(url)
    assert response.status_code == 302          # Перенаправление после выхода
    assert response.url == reverse('home')      # Перенаправление на главную страницу (LOGOUT_REDIRECT_URL)

    # Проверка наличия сообщения об успешном выходе
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Вы вышли из системы'


def test_user_logout_view_guest_redirect(client):
    """Гость может выйти (будет редирект, но без эффекта)."""
    url = reverse('users:logout')
    response = client.post(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


# 2. Тесты для представления UserRegisterView
@pytest.mark.django_db
def test_user_register_view_page_accessible(client):
    """Страница регистрации доступна для анонимного пользователя."""
    url = reverse('users:register')
    response = client.get(url)
    assert response.status_code == 200                                      # Страница доступна
    assert 'users/register.html' in [t.name for t in response.templates]    # Используется правильный шаблон


@pytest.mark.django_db
def test_user_register_view_successful_registration(client):
    """Пользователь может успешно зарегистрироваться с правильными данными."""
    url = reverse('users:register')
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'newpass123',
        'password2': 'newpass123',
    }
    response = client.post(url, data)
    assert response.status_code == 302                  # Перенаправление после успешной регистрации
    assert response.url == reverse('users:login')       # Перенаправление на страницу логина

    # Проверка, что пользователь создан
    User = get_user_model()
    assert User.objects.filter(username='newuser').exists()


@pytest.mark.django_db
def test_user_register_view_duplicate_email(client, user):
    """Регистрация с уже существующим email должна выдавать ошибку."""
    url = reverse('users:register')
    data = {
        'username': 'anotheruser',
        'email': 'test@example.com',    # email уже существует у user
        'password1': 'anotherpass123',
        'password2': 'anotherpass123',
    }
    response = client.post(url, data)
    assert response.status_code == 200                  # Страница перезагружается с ошибой
    assert response.context['form'].errors              # Форма содержит ошибки
    assert 'email' in response.context['form'].errors   # Ошибка связана с полем email


# 3. Тесты для представления ProfileView