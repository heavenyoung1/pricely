import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src.core.uow import SQLAlchemyUnitOfWork
from src.infrastructure.database.models import Base  # твои SQLAlchemy модели
from src.domain.entities import User, Product, Price

@pytest.fixture(scope='session')
def engine():
    '''In-memory SQLite для тестов'''
    engine = create_engine('sqlite:///:memory:', echo=False, future=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    clear_mappers()

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
def mock_session(self):
    '''Мокированная сессия SQLAlchemy'''
    return Mock()