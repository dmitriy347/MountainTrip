FROM python:3.11-slim

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Системные зависимости + netcat для проверки PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    postgresql-client \
    libpq-dev \
    libpq5 \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Python-зависимости (основные + dev)
COPY requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install -r requirements-dev.txt

# Копируем проект
COPY . .

# Копируем и делаем entrypoint исполняемым
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Используем entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]