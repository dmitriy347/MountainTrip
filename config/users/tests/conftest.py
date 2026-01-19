import pytest
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


User = get_user_model()

@pytest.fixture
def user(db):
    """Обычный пользователь для тестов"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def auth_client(client, user):
    """Django test client с авторизованным пользователем"""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def social_app(db):
    """
    Создаёт SocialApp для GitHub OAuth (нужно для django-allauth).
    Без этого шаблоны с {% provider_login_url %} будут падать.
    """
    try:
        site = Site.objects.get_current()
        app = SocialApp.objects.create(
            provider='github',
            name='GitHub',
            client_id='test-client-id',
            secret='test-secret',
        )
        app.sites.add(site)
        return app
    except ImportError:
        # allauth не установлен в тестах
        return None