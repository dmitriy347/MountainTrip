#!/bin/sh

# Цвета для логов
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color - сброс цвета

echo -e "${GREEN}=== SkiTrip Journal - Starting ===${NC}"

# Ждем, пока PostgreSQL будет готов, т.к. Django запускается быстрее
echo -e "${YELLOW}Waiting for PostgreSQL...${NC}"
while ! nc -z db 5432; do
  sleep 0.1
done
echo -e "${GREEN}✓ PostgreSQL started${NC}"

# Всё что ниже — только для web-сервера, не для Celery Worker
if [ "$1" != "celery" ]; then

  # Применяем миграции без запроса подтверждения
  echo -e "${YELLOW}Applying database migrations...${NC}"
  python config/manage.py migrate --noinput
  echo -e "${GREEN}✓ Migrations applied${NC}"

  # Проверяем переменную окружения DEBUG
  if [ "$DEBUG" = "True" ]; then
    # Загружаем тестовые данные из fixtures
    echo -e "${YELLOW}Loading fixtures...${NC}"
    python config/manage.py loaddata resorts.json
    python config/manage.py loaddata users.json
    python config/manage.py loaddata trips.json
    echo -e "${GREEN}✓ Test data loaded${NC}"

  # Обрабатываем медиафайлы
    # Если директория с медиафайлами существует, копируем их в новую директорию media, игнорируя ошибки
    if [ -d "config/fixtures/media/trip_photos" ]; then
      echo -e "${YELLOW}Copying media files...${NC}"
      mkdir -p config/media/trip_photos
      cp -r config/fixtures/media/trip_photos/* config/media/trip_photos/ 2>/dev/null || true
      echo -e "${GREEN}✓ Media files copied${NC}"

      # Загружаем fixture с медиа
      echo -e "${YELLOW}Loading media fixtures...${NC}"
      python config/manage.py loaddata trip_media.json
      echo -e "${GREEN}✓ Media fixtures loaded${NC}"
    else
      echo -e "${YELLOW}⚠️  fixtures/media/trip_photos not found, skipping media${NC}"
    fi
  fi

  # Собираем статику (для продакшена)
   echo -e "${YELLOW}Collecting static files...${NC}"
   python config/manage.py collectstatic --noinput
   echo -e "${GREEN}✓ Static files collected${NC}"

  # Запускаем сервер
  echo -e "${GREEN}=== Starting Django server ===${NC}"
fi

# Запускаем переданную команду (gunicorn или celery)
exec "$@"