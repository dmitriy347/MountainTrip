#!/bin/sh

# Цвета для логов
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== SkiTrip Journal - Starting ===${NC}"

# Ждем, пока PostgreSQL будет готов
echo -e "${YELLOW}Waiting for PostgreSQL...${NC}"
while ! nc -z db 5432; do
  sleep 0.1
done
echo -e "${GREEN}✓ PostgreSQL started${NC}"

# Применяем миграции
echo -e "${YELLOW}Applying database migrations...${NC}"
python manage.py migrate --noinput
echo -e "${GREEN}✓ Migrations applied${NC}"

if [ "$DEBUG" = "True" ]; then
  # Заполняем тестовыми данными (для отладки)
  echo -e "${YELLOW}Loading fixtures...${NC}"
  python manage.py loaddata resorts.json
  python manage.py loaddata users.json
  python manage.py loaddata trips.json
  python manage.py loaddata socialapp.json
  echo -e "${GREEN}✓ Test data loaded${NC}"
fi


# Собираем статику (для продакшена)
# echo -e "${YELLOW}Collecting static files...${NC}"
# python manage.py collectstatic --noinput
# echo -e "${GREEN}✓ Static files collected${NC}"

# Запускаем сервер
echo -e "${GREEN}=== Starting Django server ===${NC}"
exec "$@"