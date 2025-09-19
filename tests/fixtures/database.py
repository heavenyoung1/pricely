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
from sqlalchemy import text

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
    if not settings.TEST_NAME:
        raise RuntimeError("Тестовая БД не настроена в .env (отсутствует DB_TEST_NAME)")
    return settings

@pytest.fixture(scope="session")
def engine(test_db_settings):
    """
    Реальный движок PostgreSQL для интеграционных тестов.
    Применяет миграции Alembic к тестовой БД.
    """
    # ЯВНО указываем что хотим тестовую БД
    test_db_url = test_db_settings.get_database_url(use_test=True)
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
    # ЯВНО указываем что хотим тестовую БД для Alembic
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_settings.get_alembic_url(use_test=True))
    
    # Применяем миграции
    logger.info(f"Применение миграций к тестовой БД: {test_db_settings.TEST_NAME}")
    command.upgrade(alembic_cfg, "head")

    yield engine

    # Очищаем БД после тестов
    # logger.info(f"Очистка тестовой БД: {test_db_settings.TEST_NAME}")
    # command.downgrade(alembic_cfg, "base")
    # engine.dispose()
    # clear_mappers()

    # Вместо downgrade просто закрываем соединения
    logger.info(f"Завершение работы с тестовой БД: {test_db_settings.TEST_NAME}")
    engine.dispose()

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
    """Открываем и закрываем сессию на каждый тест и чистим БД"""
    session = session_factory()

    # Чистим все таблицы через TRUNCATE CASCADE
    #session.execute(text("TRUNCATE TABLE users, products, prices RESTART IDENTITY CASCADE;"))
    session.commit()  # ⚡ обязательно, иначе truncate не фиксируется

    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(autouse=True)
def clean_db(uow):
    with uow:
        uow.session.execute(text("TRUNCATE TABLE prices, products, users RESTART IDENTITY CASCADE"))
        uow.commit()
    yield

@pytest.fixture
def uow(session_factory, engine):
    """UoW с чисткой БД перед каждым тестом."""
    # with engine.connect() as conn:
    #     conn.execute(text("TRUNCATE TABLE users, products, prices RESTART IDENTITY CASCADE;"))
    #     conn.commit()
    return SQLAlchemyUnitOfWork(session_factory=session_factory)

@pytest.fixture
def mock_session():
    '''Мокированная сессия SQLAlchemy'''
    return Mock()