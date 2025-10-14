# 📉 Pricely

    Telegram-бот для отслеживания изменения цен на товары Ozon.
    Использует архитектуру Domain-Driven Design (DDD), паттерн Unit of Work, и чистый Dependency Injection без глобальных синглтонов.

## 🧠 Описание

**Pricely** — это Telegram-бот, который позволяет пользователям:

- добавлять товары по ссылке с Ozon,

- отслеживать текущие и предыдущие цены,

- получать уведомления при изменении стоимости.

В основе — модульная, масштабируемая архитектура с чётким разделением слоёв:

- Domain Layer — бизнес-сущности и правила;

- Application Layer — Use Cases;

- Infrastructure Layer — SQLAlchemy, репозитории, парсер, сервисы;

- Presentation Layer — Telegram-интерфейс (Aiogram).

## 🚀 Основные возможности

✅ Добавление товара по ссылке Ozon\
✅ Автоматическое обновление цен каждые N минут\
✅ Уведомление пользователя при изменении цены\
✅ Просмотр всех отслеживаемых товаров\
✅ Удаление товаров из списка\
✅ Интеграция с PostgreSQL\
✅ Безопасная работа с транзакциями через Unit of Work\
✅ Чистая Dependency Injection без контейнеров\

## 🛠 Технологии

| Компонент         | Технология                                             |
| ----------------- | ------------------------------------------------------ |
| Язык              | Python 3.13                                            |
| Telegram Bot      | Aiogram 3                                              |
| База данных       | PostgreSQL                                             |
| ORM               | SQLAlchemy 2.x                                         |
| Планировщик задач | APScheduler                                            |
| Парсер            | Selenium                                               |
| Логирование       | logging                                                |
| Архитектура       | Domain-Driven Design, Unit of Work, Repository Pattern |

## ⚙️ Установка

```bash
git clone https://github.com/heavenyoung1/pricely
cd pricely
uv sync
```

Скопируйте файл .env.example в .env

```bash
cp .env.example .env
```

Откройте файл `.env` и настройте *переменные окружения* для подключения к базе данных и других сервисов, например командой `sudo nano .env`.

Поднять Базу Данных при помощи docker-compose.
В файле `docker-compose.yml` настроены две базы данных (`pricely_db` и `pricely_test_db`). Чтобы поднять оба контейнера, используйте команду:

```bash 
docker-compose up -d
```

Это поднимет обе базы данных в фоновом режиме. Проверьте, что контейнеры работают командой:

```bash
docker ps
```

Применение миграций к БД. Можно поочередно применить миграции к `pricely_db` и `pricely_test_db` командами:

```bash
make migrate-dev     # Применить миграции на dev БД
make migrate-test    # Применить миграции на test БД
```

Либо применить миграции сразу к **двум БД** командой:
```bash
make migrate-all     # Применить миграции на обе БД
```

Ожидаемый вывод:

```bash
ALEMBIC_DATABASE_URL=$(uv run python scripts/db_url.py dev) uv run alembic upgrade head
INFO  [alembic.runtime.migration] Используем заданный ALEMBIC_DATABASE_URL: postgresql://postgres:1234@192.168.154.121:5432/pricely_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
ALEMBIC_DATABASE_URL=$(uv run python scripts/db_url.py test) uv run alembic upgrade head
INFO  [alembic.runtime.migration] Используем заданный ALEMBIC_DATABASE_URL: postgresql://postgres:1234@192.168.154.121:5433/pricely_test_db
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
Миграции успешно применены к обеим БД
```

## 🧪 Запуск тестов

Эта команда запустит все тесты и выведет подробный лог.
Для запуска тестов, выполните команду:


```bash
make tests
```

## 🔄 Запуск бота

Для запуска бота, после того как вы настроили БД и миграции, выполните команду: