# Pricely

### Локальная установка

1. Клонировать репозиторий:
```bash
git clone git@github.com:heavenyoung1/pricely.git
cd pricely
```

2. Создать файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
nano .env
```

3. Сборка и запуск через docker-compose


2. Создать виртуальное окружение и установить зависимости:
```bash
uv venv
uv pip install -r pyproject.toml
```

3. Заполнить переменные окружения в `.env`:
`nano .env`
`Ctrl + O -> Enter -> Ctrl + X`

3. Установить браузеры Playwright:
```bash
playwright install chromium
```

4. Создать файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

5. Заполнить переменные окружения в `.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=pricely_prod

BOT_TOKEN=your_telegram_bot_token
```

6. Запустить PostgreSQL и применить миграции:
```bash
docker-compose up -d db
alembic upgrade head
```

7. Запустить бота:
```bash
python -m presentation.telegram.bot
```

### Docker

1. Заполнить `.env` файл

2. Запустить всё через docker-compose:
```bash
docker-compose up -d
```

## Использование

1. Найти бота в Telegram и отправить `/start`
2. Нажать "Добавить товар" и отправить ссылку на товар
3. Бот спарсит информацию и добавит товар в отслеживание
4. При изменении цены выше порога — получить уведомление

## Проверка цен

Для запуска проверки цен всех товаров:
```bash
python main.py
```

## Разработка

### Линтинг и форматирование

```bash
ruff check .
black .
```

### Тесты

```bash
pytest
```

## Лицензия

MIT
