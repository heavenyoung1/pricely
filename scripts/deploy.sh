#!/usr/bin/env bash
set -euo pipefail

echo "== [1] Обновляем список пакетов =="
sudo apt update -y

echo "== [2] Проверяем и ставим утилиты make и docker-compose/docker compose =="
if ! command -v make >/dev/null 2>&1; then
  echo "make не найден — устанавливаю..."
  sudo apt install -y make
else
  echo "make уже установлен."
fi

# Проверяем наличие docker (демон) и compose
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker не найден — поставьте Docker Engine перед продолжением."
  echo "См.: https://docs.docker.com/engine/install/"
  exit 1
fi

# Определяем, какая именно команда compose доступна
COMPOSE_CMD=""
if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
elif docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker compose"
else
  echo "Docker Compose не найден — устанавливаю пакет docker-compose..."
  sudo apt install -y docker-compose || true
  if command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
  elif docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
  else
    echo "Не удалось обнаружить docker-compose. Проверьте установку Docker Compose (v1 или v2) и повторите."
    exit 1
  fi
fi
echo "Будет использоваться команда compose: '${COMPOSE_CMD}'"

echo "== [3] Проверяем членство пользователя в группе docker =="
CURRENT_USER="${SUDO_USER:-$USER}"
if id -nG "$CURRENT_USER" | grep -qw docker; then
  echo "Пользователь ${CURRENT_USER} уже в группе docker."
else
  echo "Добавляю ${CURRENT_USER} в группу docker..."
  sudo usermod -aG docker "$CURRENT_USER"
  echo "✅ Готово. Перезайдите в сессию (или выполните 'newgrp docker') и запустите скрипт снова."
  exit 0
fi

echo "== [4] UV: проверяем наличие утилиты uv =="
if command -v uv >/dev/null 2>&1; then
  echo "uv уже установлен."
else
  echo "uv не найден — устанавливаю..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Подхватываем PATH текущей сессии, если установщик прописал в .bashrc/.profile
  if [ -f "$HOME/.bashrc" ]; then source "$HOME/.bashrc" || true; fi
  if [ -f "$HOME/.profile" ]; then source "$HOME/.profile" || true; fi
  if ! command -v uv >/dev/null 2>&1; then
    echo "uv установлен, но не в PATH текущей сессии. Перезапустите терминал ИЛИ выполните 'source ~/.bashrc' и запустите скрипт снова."
    exit 0
  fi
fi

echo "== [5] Синхронизируем виртуальное окружение через uv =="
uv sync  # создаст .venv и поставит зависимости

echo "== [6] Проверяем Google Chrome =="
if command -v google-chrome-stable >/dev/null 2>&1 || command -v google-chrome >/dev/null 2>&1 || command -v chrome >/dev/null 2>&1; then
  echo "Chrome уже установлен."
else
  echo "Chrome не найден — скачиваю сборку for-testing..."
  CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.122/linux64/chrome-linux64.zip"
  curl -LsSf -o chrome-linux64.zip "$CHROME_URL"
  unzip -o chrome-linux64.zip -d chrome-linux64
  chmod +x ./chrome-linux64/chrome-linux64
  sudo mv ./chrome-linux64/chrome-linux64 /usr/local/bin/chrome
  rm -f chrome-linux64.zip
  echo "Chrome установлен как /usr/local/bin/chrome"
fi

echo "== [7] Проверяем ChromeDriver =="
if command -v chromedriver >/dev/null 2>&1; then
  echo "chromedriver уже установлен."
else
  echo "chromedriver не найден — скачиваю соответствующую версию..."
  CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.122/linux64/chromedriver-linux64.zip"
  curl -LsSf -o chromedriver.zip "$CHROMEDRIVER_URL"
  unzip -o chromedriver.zip -d chrome-linux64
  chmod +x ./chrome-linux64/chromedriver-linux64/chromedriver
  sudo mv ./chrome-linux64/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
  rm -f chromedriver.zip
  echo "chromedriver установлен как /usr/local/bin/chromedriver"
fi

echo "== [8] Создаём пустой proxy.json (если нет) =="
PROXY_FILE="src/infrastructure/parsers/proxy.json"
if [ ! -f "$PROXY_FILE" ]; then
  mkdir -p "$(dirname "$PROXY_FILE")"
  : > "$PROXY_FILE"
  echo "Создан пустой $PROXY_FILE — при необходимости заполни."
else
  echo "$PROXY_FILE уже существует."
fi

echo "== [9] Готовим .env =="
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
    echo "Создан .env из .env.example"
  else
    echo "В репозитории нет .env.example — создаю пустой .env"
    : > .env
  fi
else
  echo ".env уже существует."
fi

echo "== [10] Открой .env для настройки (база, токены и пр.) =="
echo "Нажми Ctrl+X для выхода, Y для сохранения (если были изменения)."
nano .env

echo "== [11] Поднимаем базу/зависимости Docker Compose =="
${COMPOSE_CMD} -f docker-compose.yml up -d

echo "== [12] Проверяем контейнеры =="
docker ps

echo "== [13] Миграции БД =="
make migrate-all

echo "== [14] Тесты =="
make tests

echo "== [15] Устанавливаем и включаем systemd-службу pricely =="
# предполагаем, что юнит лежит в репозитории по пути ./scripts/pricely.service
SERVICE_SRC="./scripts/pricely.service"
if [ ! -f "$SERVICE_SRC" ]; then
  echo "⚠️  Не найден $SERVICE_SRC. Уточни путь к юниту в репозитории."
  exit 1
fi

SERVICE_NAME="pricely.service"
SERVICE_DST="/etc/systemd/system/${SERVICE_NAME}"
TMP_UNIT="$(mktemp)"

# 1) копируем исходник во временный файл
cp "$SERVICE_SRC" "$TMP_UNIT"

# 2) подправляем юнит под текущую машину
# - актуальный WorkingDirectory = текущий репозиторий
WD="$(pwd)"
# - актуальный пользователь
SERV_USER="$CURRENT_USER"
# - корректный PATH в среде systemd (чтобы находились uv/make/docker)
SYS_PATH="/home/${SERV_USER}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"

# правки через sed (idempotent)
sed -i \
  -e "s|^User=.*|User=${SERV_USER}|" \
  -e "s|^Group=.*|Group=docker|" \
  -e "s|^WorkingDirectory=.*|WorkingDirectory=${WD}|" \
  -e "s|^Environment=.*|Environment=PATH=${SYS_PATH}|" \
  -e "s|^After=network\.target docker\.service|After=network-online.target docker.service|" \
  "$TMP_UNIT"

# если у нас compose v2 — меняем docker-compose -> docker compose
if [ "$COMPOSE_CMD" = "docker compose" ]; then
  sed -i -e 's|/usr/bin/docker-compose|/usr/bin/docker compose|g' "$TMP_UNIT"
fi

# 3) ставим юнит в систему
echo "Копирую юнит в ${SERVICE_DST}…"
sudo cp "$TMP_UNIT" "$SERVICE_DST"
rm -f "$TMP_UNIT"

# 4) применяем и включаем
sudo systemctl daemon-reload
sudo systemctl enable --now "${SERVICE_NAME}"

echo "== [16] Статус службы =="
systemctl --no-pager --full status "${SERVICE_NAME}" || true
echo "Логи (последние строки):"
journalctl -u "${SERVICE_NAME}" -n 50 --no-pager || true

echo "✅ Готово! Окружение собрано, служба установлена и запущена."
