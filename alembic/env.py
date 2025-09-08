from logging.config import fileConfig
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

# Проверяем, передан ли URL через переменную окружения
custom_url = os.getenv("ALEMBIC_DATABASE_URL")
if custom_url:
    config.set_main_option('sqlalchemy.url', custom_url)
else:
    # Используем URL по умолчанию из настроек
    config.set_main_option('sqlalchemy.url', db_settings.get_db_url())

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
