import pytest
import subprocess
from alembic.config import Config
from alembic import command
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session ,clear_mappers
from src.core.uow import SQLAlchemyUnitOfWork
from src.core import DataBaseSettings, DatabaseConnection
from src.infrastructure.database.models import Base  # SQLAlchemy модели
from src.domain.entities import User, Product, Price

import logging

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@pytest.fixture(scope="session")
def test_db_settings():
    """Фикстура для настроек тестовой БД."""
    settings = DataBaseSettings()
    if not settings.is_test_db_configured:
        raise RuntimeError("Тестовая БД не настроена в .env (отсутствует DB_TEST_NAME)")
    return settings

@pytest.fixture(scope="session")
def engine(test_db_settings):
    """
    Реальный движок PostgreSQL для интеграционных тестов.
    Применяет миграции Alembic к тестовой БД.
    """
    test_db_url = test_db_settings.get_test_db_url()
    logger.info(f"Создание движка для тестовой БД: {test_db_url}")
    
    engine = create_engine(
        test_db_url,
        echo=False,  # Можно установить True для отладки SQL
        future=True,
        pool_pre_ping=True,
    )

    # Проверяем подключение
    db = DatabaseConnection(test_db_settings)
    if not db.test_connection(db_url=test_db_url):
        raise RuntimeError(f"Не удалось подключиться к тестовой БД: {test_db_url}")

    # Настраиваем Alembic для тестовой БД
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_settings.get_alembic_url(use_test=True))
    
    # Применяем миграции
    logger.info(f"Применение миграций к тестовой БД: {test_db_settings.TEST_NAME}")
    command.upgrade(alembic_cfg, "head")

    yield engine

    # Очищаем БД после тестов
    logger.info(f"Очистка тестовой БД: {test_db_settings.TEST_NAME}")
    command.downgrade(alembic_cfg, "base")
    engine.dispose()
    clear_mappers()

@pytest.fixture
def session_factory(engine):
    """Фабрика сессий для тестов."""
    return sessionmaker(
        bind=engine,
        class_=Session,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


@pytest.fixture
def db_session(session_factory):
    '''Открываем и закрываем сессию на каждый тест'''
    session = session_factory()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def uow(session_factory):
    '''UoW с тестовой фабрикой'''
    return SQLAlchemyUnitOfWork(session_factory=session_factory)

@pytest.fixture
def mock_session():
    '''Мокированная сессия SQLAlchemy'''
    return Mock()