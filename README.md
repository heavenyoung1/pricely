# 📉 Pricely

![Python version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)
![Status](https://img.shields.io/badge/status-in%20development-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![codecov](https://img.shields.io/codecov/c/heavenyoung1/pricely.svg)

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
✅ Чистая Dependency Injection без контейнеров

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

## 🏗 Строение базы данных

![Схема базы данных](./doc/images/pricely_db_1.png)

## 📐 Архитектура приложения

<div style="text-align: center;">
    <img src="./doc/images/scheme.png" alt="Архитектура приложения" width="500px" />
</div>

## ⚙️ Установка

1. Клонирование репозитория

```bash
git clone https://github.com/heavenyoung1/pricely
cd pricely
```

2. Активация виртуального окружения при помощи утилиты `uv`
```bash
uv sync
```

3. Конфигурация подключений

Скопируйте файл `.env.example` в `.env`

```bash
cp .env.example .env
```

Откройте файл `.env` и настройте *переменные окружения* для подключения к *базе данных* и другим сервисам.

```bash
sudo nano .env
```

4. Поднятие баз данных с помощью `docker-compose`

В файле `docker-compose.yml` настроены *две* базы данных (`pricely_db` и `pricely_test_db`). Чтобы поднять оба контейнера, используйте команду:

```bash 
docker-compose up -d
```

Это поднимет обе базы данных в фоновом режиме. Проверьте, что контейнеры работают командой:

```bash
docker ps
```

5. Применение миграций к БД.

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

6. Запуск тестов

Эта команда запустит все тесты и выведет подробный лог.
Для запуска тестов, выполните команду:

```bash
make tests
```

7. Запуск бота

Для запуска бота, после того как вы настроили БД и миграции, выполните команду:

```bash
make bot
```

## ⚙️ Развертывание при помощи скрипта

```
git clone https://github.com/heavenyoung1/pricely
cd pricely
sudo chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## Ввод данных
Во время выполнения скрипта вам будет предложено:
 - Заполнить файл `proxy.json` с данными прокси-сервера (если необходимо). Proxy имеют подобный вид

 ```bash
 [
  {
    "proxy": "192.168.101.1:2000",
    "user": "LOGIN",
    "password": "PASSWORD"
  },
  {
    "proxy": "192.168.101.1:2000",
    "user": "LOGIN",
    "password": "PASSWORD"
  }
 ]
 ```

- Настроить файл .env, который будет содержать настройки подключения к базе данных и другие переменные окружения. После этого откроется редактор `nano` для изменения файла .`env.` Убедитесь, что все параметры в файле настроены правильно.
