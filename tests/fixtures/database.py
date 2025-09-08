import pytest
import subprocess
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src.core.uow import SQLAlchemyUnitOfWork
from src.core import DataBaseSettings
from src.infrastructure.database.models import Base  # SQLAlchemy модели
from src.domain.entities import User, Product, Price

@pytest.fixture(scope="session")
def engine():
    """
    Реальный движок PostgreSQL для интеграционных тестов.
    Использует тестовую БД из docker-compose.
    """
    settings = DataBaseSettings()
    url = settings.get_test_db_url()  # Берём строку подключения из .env

    engine = create_engine(url, echo=False, future=True)

    # создаём схему (если нужно — как alembic миграции)
    Base.metadata.create_all(engine)

    yield engine

    # после тестов можно подчистить
    Base.metadata.drop_all(engine)
    clear_mappers()

# Вот эта фикстура ломает все тесты, она нужна чтобы для тестов так же использовать Alembic
# @pytest.fixture(scope="session", autouse=True)
# def apply_migrations():
#     """Перед всеми тестами прогоняем миграции в тестовой БД"""
#     subprocess.run(
#         ["uv", "run", "alembic", "upgrade", "head", "-x", f"url={DataBaseSettings().get_test_db_url()}"],
#         check=True
#     )
#     yield

@pytest.fixture
def session_factory(engine):
    '''Фабрика сессий для тестов'''
    return sessionmaker(bind=engine, expire_on_commit=False)


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