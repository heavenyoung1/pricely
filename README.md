# 📉 Pricely

# Структура проекта

price_monitor/
├── domain/
│   ├── __init__.py
│   ├── entities.py          # Бизнес-сущности
│   ├── interfaces.py        # Абстракции/интерфейсы
│   └── services.py          # Бизнес-логика
├── infrastructure/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py        # ORM модели
│   │   └── repository.py    # Реализация репозитория
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py          # Базовый парсер
│   │   └── site_parsers.py  # Парсеры для конкретных сайтов
│   ├── telegram/
│   │   ├── __init__.py
│   │   └── bot.py           # Telegram bot
│   └── scheduler/
│       ├── __init__.py
│       └── tasks.py         # Фоновые задачи
├── application/
│   ├── __init__.py
│   ├── use_cases.py         # Случаи использования
│   └── dto.py               # Data Transfer Objects
├── presentation/
│   ├── __init__.py
│   ├── handlers.py          # Обработчики команд бота
│   └── formatters.py        # Форматирование сообщений
├── config/
│   ├── __init__.py
│   └── settings.py          # Конфигурация
└── main.py                  # Точка входа
