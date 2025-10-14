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
