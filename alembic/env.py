from logging.config import fileConfig
import logging
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from src.core.db_connection import DataBaseSettings
from src.infrastructure.database.models import Base
from src.core.db_connection import db_settings
from alembic import context
import os


# Загружаем переменные окружения из .env
load_dotenv()

# Настройка логгера Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.runtime.migration")

# Получаем настройки базы данных
db_settings = DataBaseSettings()

# Определяем URL базы данных
# Приоритет: ALEMBIC_DATABASE_URL из командной строки > автоматическое определение
db_url = os.getenv("ALEMBIC_DATABASE_URL")
if not db_url:
    # Если ALEMBIC_DATABASE_URL не задан, определяем URL через DataBaseSettings
    use_test = (
        os.getenv("TEST_DATABASE_URL") is not None or db_settings.is_test_db_configured
    )
    db_url = db_settings.get_alembic_url(use_test=use_test)
    logger.info(f"ALEMBIC_DATABASE_URL не задан, используем: {db_url}")
else:
    logger.info(f"Используем заданный ALEMBIC_DATABASE_URL: {db_url}")

# Устанавливаем URL в конфигурацию Alembic
config.set_main_option("sqlalchemy.url", db_url)

# Импортируем модели
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
