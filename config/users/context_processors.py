from django.conf import settings

def auth_providers(request):
    """Добавляет в контекст шаблонов список провайдеров аутентификации."""
    return {
        'GITHUB_LOGIN_ENABLED': settings.GITHUB_LOGIN_ENABLED,
    }