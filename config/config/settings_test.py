from .settings import *

# В тестах ставим огромные лимиты, чтобы throttling не срабатывал
REST_FRAMEWORK = REST_FRAMEWORK.copy()
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "anon": "100000/minute",
    "user": "100000/minute",
    "auth": "100000/minute",
    "trips_create": "100000/hour",
}

# Celery в тестах: выполнять задачи синхронно, без реального брокера
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True