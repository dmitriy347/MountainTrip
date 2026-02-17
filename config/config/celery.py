import os
from celery import Celery

# Указываем Django settings модуль для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создаём экземпляр Celery c именем "config"
app = Celery("config")

# Загружаем настройки из Django settings с префиксом CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим tasks.py во всех установленных приложениях Django
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Тестовая задача для проверки работы Celery."""
    print(f"Request: {self.request!r}")
