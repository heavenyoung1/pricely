#!/bin/bash

# 1. Клонирование репозитория (если ещё не сделано)
if [ ! -d "pricely" ]; then
  echo "Клонируем репозиторий..."
  git clone https://github.com/heavenyoung1/pricely
  cd pricely
else
  echo "Репозиторий уже клонирован. Переходим в каталог..."
  cd pricely
fi

# 2. Проверка наличия утилиты uv
if command -v uv &> /dev/null; then
  echo "Утилита uv уже установлена, пропускаем установку."
else
  echo "Утилита uv не найдена, скачиваем..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  echo "Утилита uv установлена. Необходимо перезапустить терминал для активации."
  echo "Закройте и откройте терминал или выполните команду: source ~/.bashrc"
  exit 0  # Прерываем выполнение скрипта, чтобы пользователь перезапустил терминал
fi

# 3. Активация виртуального окружения при помощи утилиты `uv`
echo "Активируем виртуальное окружение с помощью uv..."
uv sync

# 4. Проверка наличия установленного Google Chrome
if command -v google-chrome &> /dev/null; then
  echo "Google Chrome уже установлен, пропускаем установку."
else
  echo "Google Chrome не найден, скачиваем..."
  CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.122/linux64/chrome-linux64.zip"
  curl -LsSf -o chrome-linux64.zip "$CHROME_URL"
  unzip chrome-linux64.zip -d chrome-linux64
  chmod +x ./chrome-linux64/chrome-linux64
  sudo mv ./chrome-linux64/chrome-linux64 /usr/local/bin/chrome
  rm chrome-linux64.zip
  echo "Google Chrome установлен успешно"
fi

# 5. Проверка наличия установленного ChromeDriver
if command -v chromedriver &> /dev/null; then
  echo "ChromeDriver уже установлен, пропускаем установку."
else
  echo "ChromeDriver не найден, скачиваем..."
  CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.122/linux64/chromedriver-linux64.zip"
  curl -LsSf -o chromedriver.zip "$CHROMEDRIVER_URL"
  unzip chromedriver.zip -d chrome-linux64
  chmod +x ./chrome-linux64/chromedriver-linux64/chromedriver
  sudo mv ./chrome-linux64/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
  rm chromedriver.zip
  echo "ChromeDriver скачан и установлен"
fi

# 6. Создание пустого файла proxy.json
PROXY_FILE="src/infrastructure/parsers/proxy.json"
if [ ! -f "$PROXY_FILE" ]; then
  echo "Создаём пустой файл proxy.json..."
  mkdir -p "$(dirname "$PROXY_FILE")"
  
  # Создаем пустой файл
  touch "$PROXY_FILE"
  echo "Файл proxy.json создан. Пожалуйста, заполните его при необходимости."
else
  echo "Файл proxy.json уже существует."
fi

# 7. Конфигурация подключений (создание .env файла)
if [ ! -f ".env" ]; then
  echo "Создаём файл .env из .env.example..."
  cp .env.example .env
else
  echo ".env уже существует"
fi

# Открываем файл .env для редактирования и настройки (пользователь должен сделать это вручную)
echo "Откройте файл .env для настройки подключений к базе данных и другим сервисам:"
nano .env

# 8. Поднятие баз данных с помощью `docker-compose`
echo "Запускаем Docker контейнеры для баз данных..."
docker-compose up -d

# Подтверждаем, что контейнеры работают
echo "Проверяем, что контейнеры работают..."
docker ps

# 9. Применение миграций к БД
echo "Применяем миграции к БД..."
make migrate-all

# 10. Запуск тестов
echo "Запускаем тесты..."
make tests

# 11. Завершаем процесс развертывания
echo "Все компоненты собраны и настроены успешно!"

# 12. Запуск бота
echo "Запускаем бота..."
make bot

# 13. Завершаем процесс
echo "Процесс развертывания завершён!"

