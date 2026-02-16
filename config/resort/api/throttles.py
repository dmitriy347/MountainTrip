from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AuthThrottle(AnonRateThrottle):
    """
    Ограничение попыток получения JWT токена
    Защита от bruteforce атак
    """

    scope = "auth"  # Имя кастомного лимита


class TripCreateThrottle(UserRateThrottle):
    """
    Ограничение создания поездок
    Защита от спама
    """

    scope = "trips_create"  # Имя кастомного лимита
