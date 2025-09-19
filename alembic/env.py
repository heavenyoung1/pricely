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

load_dotenv()

# Настройка логгера Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.runtime.migration")

# Настройки БД
db_settings = DataBaseSettings()
use_test_db = os.getenv("TEST_DATABASE_URL") or db_settings.is_test_db_configured
db_url = os.getenv("DATABASE_URL", db_settings.get_alembic_url(use_test=use_test_db))

config.set_main_option("sqlalchemy.url", db_url)

logger.info(f"Используем БД - {db_url}")

# Импортируем модели
target_metadata = Base.metadata

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


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
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
