import pytest

from src.infrastructure.database.repositories import (
    ProductRepositoryImpl,
    PriceRepositoryImpl,
    UserRepositoryImpl
)
import logging
logger = logging.getLogger(__name__)

# ----- РЕПОЗИТОРИИ ДЛЯ ИНТЕГРАЦИОННЫХ - ТЕСТОВ С DB-SESSION -----  #

@pytest.fixture
def product_repo(db_session): # ← Использует реальную сессию с SQLite
    '''Фикстура репозитория продуктов с сессией.'''
    return ProductRepositoryImpl(session=db_session)

@pytest.fixture
def price_repo(db_session): # ← Использует реальную сессию с SQLite
    '''Фикстура репозитория продуктов с сессией.'''
    return PriceRepositoryImpl(session=db_session)

@pytest.fixture
def user_repo(db_session): # ← Использует реальную сессию с SQLite
    '''Фикстура репозитория продуктов с сессией.'''
    return UserRepositoryImpl(session=db_session)

# ----- ЗАМОКАНЫЕ РЕПОЗИТОРИИ ДЛЯ UNIT - ТЕСТОВ -----  #

@pytest.fixture
def mock_product_repo(mock_session): # ← Использует мокированную сессию
    '''Фикстура репозитория товаров с замоканной сессией.'''
    logger.debug(f'TYPE OF MOCK PRODUCT REPO {type(mock_product_repo)}')
    return ProductRepositoryImpl(session=mock_session)

@pytest.fixture
def mock_price_repo(mock_session): # ← Использует мокированную сессию
    '''Фикстура репозитория товаров с замоканной сессией.'''
    return PriceRepositoryImpl(session=mock_session)

@pytest.fixture
def mock_user_repo(mock_session): # ← Использует мокированную сессию
    '''Фикстура репозитория товаров с замоканной сессией.'''
    return UserRepositoryImpl(session=mock_session)