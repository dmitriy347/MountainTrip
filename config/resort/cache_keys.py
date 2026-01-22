"""Централизованное управление ключами кэша.
Все ключи кэша проекта хранятся здесь.
"""


class CacheKeys:
    """Класс для генерации ключей кэша."""

    # Префиксы для разных типов данных
    PREFIX_RESORT = "resort"
    PREFIX_TRIP = "trip"

    RESORT_LIST = f"{PREFIX_RESORT}:list"

    @staticmethod
    def resort_trips_counts(resort_id):
        """Генерирует ключ кэша для счетчиков поездок курорта по его ID."""
        return f"{CacheKeys.PREFIX_RESORT}:{resort_id}:trips_counts"


class CacheTimeouts:
    """Класс для хранения таймаутов кэша в секундах."""

    RESORT_LIST = 60 * 10  # 10 минут
    RESORT_TRIPS_COUNTS = 60 * 10  # 10 минут
