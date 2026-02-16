from rest_framework.throttling import AnonRateThrottle


class AuthThrottle(AnonRateThrottle):
    """
    Ограничение попыток получения JWT токена
    Защита от bruteforce атак
    """

    scope = "auth"  # Имя кастомного лимита
