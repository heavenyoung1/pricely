import pytest
import logging
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import MagicMock
from pydantic import HttpUrl

from src.infrastructure.database.repositories import ProductRepositoryImpl, PriceRepositoryImpl, UserRepositoryImpl
from src.infrastructure.database.models import Base, ORMProduct, ORMUser, ORMPrice
from src.application.dto import ProductDTO, PriceDTO, UserDTO
from src.domain.entities import Product, Price, User
from src.core.uow import SQLAlchemyUnitOfWork
from src.infrastructure.parsers import OzonParser
from src.infrastructure.services import ProductService

pytest_plugins = [
    'fixtures.database',
    'fixtures.product',
    'fixtures.price', 
    'fixtures.user',
    'fixtures.service',
]

# Другие полезные методы:
# mock_method.assert_called()          # Был ли вызван хотя бы раз
# mock_method.assert_called_with(args) # Был ли вызван с конкретными аргументами (последний вызов)
# mock_method.assert_not_called()      # НЕ был вызван

# ----- # ----- # ----- Общие настройки ----- # ----- # ----- #

@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

# ----- # ----- # ----- МОК ДЛЯ ПАРСЕРА # ----- # ----- # ----- #

@pytest.fixture
def mock_parser():
    parser = MagicMock()
    parser.parse_product.return_value = {
        'id': 'p1',
        'name':'Test Product',
        'image_url': 'https://example.com/image.jpg',
        'rating': 4.5,
        'categories': ['cat1', 'cat2'],
        'price_with_card': 100,
        'price_without_card': 120,
        'price_default': 150,
    }
    return parser

# ----- # ----- # ----- Product Service ----- # ----- # ----- #

@pytest.fixture
def product_service(uow):
    '''Фикстура для ProductService с реальным UnitOfWork.'''
    return ProductService(uow_factory=lambda: uow)

@pytest.fixture
def mock_product_service():
    return MagicMock()  # Полностью замоканный объект

# ----- # ----- # ----- MOCK UOW ----- # ----- # ----- #

@pytest.fixture(scope="function")
def mock_uow(mock_product_repo, mock_price_repo, mock_user_repo):
    '''Мок для UnitOfWork.'''
    mock_uow = MagicMock()
    mock_uow.product_repository.return_value = mock_product_repo
    mock_uow.price_repository.return_value = mock_price_repo
    mock_uow.user_repository.return_value = mock_user_repo
    mock_uow.__enter__.return_value = mock_uow
    mock_uow.__exit__.return_value = None
    print(f"Type of mock_uow.session before assignment: {type(mock_uow.session)}")
    return mock_uow

@pytest.fixture(scope="function")
def mock_session():
    session = MagicMock(spec=Session)
    print(f"Type of session.merge in mock_session: {type(session.merge)}")
    return session

@pytest.fixture(scope="function")
def mock_product_repo(mock_session):
    repo = ProductRepositoryImpl(mock_session)
    print(f"Type of repo.session.merge in mock_product_repo: {type(repo.session.merge)}")
    return repo

@pytest.fixture(scope="function")
def mock_price_repo(mock_session):
    repo = PriceRepositoryImpl(mock_session)
    print(f"Type of repo.session.merge in mock_price_repo: {type(repo.session.merge)}")
    return repo

@pytest.fixture(scope="function")
def mock_user_repo(mock_session):
    repo = UserRepositoryImpl(mock_session)
    print(f"Type of repo.session.merge in mock_user_repo: {type(repo.session.merge)}")
    return repo

# ----- # ----- # ----- Репозитории для интеграционного тестирования ----- # ----- # ----- #

@pytest.fixture
def product_repo(session):
    '''Фикстура репозитория продуктов с сессией.'''
    return ProductRepositoryImpl(session=session)

@pytest.fixture
def price_repo(session):
    '''Фикстура репозитория продуктов с сессией.'''
    return PriceRepositoryImpl(session=session)

@pytest.fixture
def user_repo(session):
    '''Фикстура репозитория продуктов с сессией.'''
    return UserRepositoryImpl(session=session)





