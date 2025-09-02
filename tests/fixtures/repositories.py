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