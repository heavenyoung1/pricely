#!/bin/bash
set -e  # останавливаем выполнение при первой же ошибке

echo "🚀 Начинаем деплой..."

# 1. Обновляем код
echo "📥 Обновляем репозиторий..."
git fetch --all
git reset --hard origin/main   # если у тебя ветка называется master — поменяй на master

# 2. Останавливаем и удаляем контейнеры
echo "🛑 Останавливаем и удаляем старые контейнеры..."
make down

# 3. Чистим мусор Docker (опционально)
echo "🧹 Чистим неиспользуемые образы и контейнеры..."
docker system prune -af --volumes

# 4. Поднимаем новые контейнеры
echo "🐳 Поднимаем контейнеры..."
make up

# 5. Ждём пока Postgres станет доступным
echo "⏳ Ждём готовности Postgres..."
until docker exec pricely_postgres_dev pg_isready -U postgres > /dev/null 2>&1; do
  sleep 2
done
until docker exec pricely_postgres_test pg_isready -U postgres > /dev/null 2>&1; do
  sleep 2
done
echo "✅ Postgres готов!"

# 6. Применяем миграции (и для dev, и для test)
echo "📜 Применяем миграции..."
make migrate-all

# 7. (опционально) Прогоняем тесты
echo "🧪 Запускаем тесты..."
make test || { echo "❌ Тесты упали!"; exit 1; }

echo "🎉 Деплой завершён успешно!"
