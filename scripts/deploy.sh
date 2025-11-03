#!/usr/bin/env bash
set -euo pipefail

echo "== [1] apt update =="
sudo apt update -y

echo "== [2] Утилиты (make, unzip, curl, nano, docker-compose v1) =="
# make
if ! command -v make >/dev/null 2>&1; then
  sudo apt install -y make
fi
# unzip
if ! command -v unzip >/dev/null 2>&1; then
  sudo apt install -y unzip
fi
# curl
if ! command -v curl >/dev/null 2>&1; then
  sudo apt install -y curl
fi
# nano
if ! command -v nano >/dev/null 2>&1; then
  sudo apt install -y nano
fi
# docker-compose (только v1 из apt)
if ! command -v docker-compose >/dev/null 2>&1; then
  echo "Устанавливаю docker-compose (apt)…"
  sudo apt install -y docker-compose
fi
COMPOSE_CMD="docker-compose"
echo "Будет использоваться: ${COMPOSE_CMD}"

echo "== [3] Пользователь в группе docker =="
CURRENT_USER="${SUDO_USER:-$USER}"
if id -nG "$CURRENT_USER" | grep -qw docker; then
  echo "${CURRENT_USER} уже в группе docker."
else
  echo "Добавляю ${CURRENT_USER} в группу docker…"
  sudo usermod -aG docker "$CURRENT_USER"
  echo "➡️  Перезайди в сессию (или 'newgrp docker') и перезапусти скрипт."
  exit 0
fi

echo "== [4] uv (без sudo) =="
if command -v uv >/dev/null 2>&1; then
  echo "uv уже установлен."
else
  echo "Ставлю uv…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # подхватываем PATH для текущей сессии
  [ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" || true
  [ -f "$HOME/.profile" ] && source "$HOME/.profile" || true
  if ! command -v uv >/dev/null 2>&1; then
    echo "uv установлен, но не в PATH. Выполни 'source ~/.bashrc' и перезапусти скрипт."
    exit 0
  fi
fi

echo "== [5] uv sync (.venv и зависимости) =="
uv sync

echo "== [6] Google Chrome (for-testing) =="
if command -v google-chrome-stable >/dev/null 2>&1 || command -v google-chrome >/dev/null 2>&1 || command -v chrome >/dev/null 2>&1; then
  echo "Chrome уже установлен."
else
  CHROME_URL="https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.122/linux64/chrome-linux64.zip"
  curl -LsSf -o chrome-linux64.zip "$CHROME_URL"
  unzip -o chrome-linux64.zip -d chrome-linux64
  chmod +x ./chrome-linux64/chrome-linux64
  sudo mv ./chrome-linux64/chrome-linux64 /usr/local/bin/chrome
  rm -f chrome-linux64.zip
  echo "Chrome установлен как /usr/local/bin/chrome"
fi

echo "== [7] Chromedriver =="
if command -v chromedriver >/dev/null 2>&1; then
  echo "chromedriver уже установлен."
else
  CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/141.0.7390.122/linux64/chromedriver-linux64.zip"
  curl -LsSf -o chromedriver.zip "$CHROMEDRIVER_URL"
  unzip -o chromedriver.zip -d chrome-linux64
  chmod +x ./chrome-linux64/chromedriver-linux64/chromedriver
  sudo mv ./chrome-linux64/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
  rm -f chromedriver.zip
  echo "chromedriver установлен как /usr/local/bin/chromedriver"
fi

echo "== [8] proxy.json =="
PROXY_FILE="src/infrastructure/parsers/proxy.json"
if [ ! -f "$PROXY_FILE" ]; then
  mkdir -p "$(dirname "$PROXY_FILE")"
  : > "$PROXY_FILE"
  echo "Создан пустой $PROXY_FILE"
else
  echo "$PROXY_FILE уже существует."
fi

echo "== [9] .env =="
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
    echo "Создан .env из .env.example"
  else
    : > .env
    echo "Создан пустой .env"
  fi
else
  echo ".env уже существует."
fi

echo "== [10] Открой .env для настройки (Ctrl+X → Y) =="
nano .env

echo "== [11] Docker зависимости (Makefile: up) =="
make up

echo "== [12] Миграции (Makefile: migrate-all) =="
make migrate-all

echo "== [13] Тесты (Makefile: tests) =="
make tests

echo "== [14] Установка systemd-сервиса из репозитория =="
SERVICE_SRC="./scripts/pricely.service"
if [ ! -f "$SERVICE_SRC" ]; then
  echo "❌ Не найден $SERVICE_SRC — проверь путь."
  exit 1
fi

SERVICE_NAME="pricely.service"
SERVICE_DST="/etc/systemd/system/${SERVICE_NAME}"
TMP_UNIT="$(mktemp)"
cp "$SERVICE_SRC" "$TMP_UNIT"

# Подстройка юнита под текущую машину:
WD="$(pwd)"
SERV_USER="${SUDO_USER:-$USER}"
SYS_PATH="/home/${SERV_USER}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"

# Чиним ключевые поля (оставляем docker-compose как в исходнике)
sed -i \
  -e "s|^User=.*|User=${SERV_USER}|" \
  -e "s|^Group=.*|Group=docker|" \
  -e "s|^WorkingDirectory=.*|WorkingDirectory=${WD}|" \
  -e "s|^Environment=.*|Environment=PATH=${SYS_PATH}|" \
  -e "s|^After=network\.target docker\.service|After=network-online.target docker.service|" \
  "$TMP_UNIT"

echo "Копирую юнит в ${SERVICE_DST}…"
sudo cp "$TMP_UNIT" "$SERVICE_DST"
rm -f "$TMP_UNIT"

echo "== [15] Включаю и запускаю службу =="
sudo systemctl daemon-reload
sudo systemctl enable --now "${SERVICE_NAME}"

echo "== [16] Статус и последние логи =="
systemctl --no-pager --full status "${SERVICE_NAME}" || true
journalctl -u "${SERVICE_NAME}" -n 50 --no-pager || true

echo "✅ Готово: окружение собрано, контейнеры подняты (docker-compose через make), миграции/тесты выполнены, служба установлена и запущена."
