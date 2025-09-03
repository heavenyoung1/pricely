import pytest

from src.infrastructure.database.repositories import (
    ProductRepositoryImpl,
    PriceRepositoryImpl,
    UserRepositoryImpl
)

@pytest.fixture
def product_repo(db_session):
    '''Фикстура репозитория продуктов с сессией.'''
    return ProductRepositoryImpl(session=db_session)

@pytest.fixture
def price_repo(db_session):
    '''Фикстура репозитория продуктов с сессией.'''
    return PriceRepositoryImpl(session=db_session)

@pytest.fixture
def user_repo(db_session):
    '''Фикстура репозитория продуктов с сессией.'''
    return UserRepositoryImpl(session=db_session)

@pytest.fixture
def mock_product_repo(mock_session):
    '''Фикстура репозитория товаров с замоканной сессией.'''
    return ProductRepositoryImpl(session=mock_session)

@pytest.fixture
def mock_price_repo(mock_session):
    '''Фикстура репозитория товаров с замоканной сессией.'''
    return PriceRepositoryImpl(session=mock_session)

@pytest.fixture
def mock_user_repo(mock_session):
    '''Фикстура репозитория товаров с замоканной сессией.'''
    return UserRepositoryImpl(session=mock_session)