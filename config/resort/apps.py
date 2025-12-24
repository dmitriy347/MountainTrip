from django.apps import AppConfig


class ResortConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resort'

    def ready(self):
        """Импорт сигналов при готовности приложения."""
        import resort.signals