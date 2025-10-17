import pytest
from pydantic import HttpUrl

from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct


@pytest.fixture
def product():
    '''Фикстура тестового доменного Product'''
    return Product(
        id='p1',
        user_id='u1',
        #price_id='pr1',
        name='Test Product',
        link='https://example.com/product',
        image_url='https://example.com/image.jpg',
        rating=4.5,
        categories='cat1, cat2'
    )

@pytest.fixture
def orm_product():
    '''Фикстура тестового ORM Product с JSON-сериализованными категориями'''
    return ORMProduct(
        id='p1',
        name='Test Product',
        link='https://example.com/product',
        image_url='https://example.com/image.jpg',
        rating=4.5,
        categories='cat1, cat2'
    )

@pytest.fixture
def product_integration():
    '''Фикстура тестового доменного Product'''
    return Product(
        id='p1',
        user_id='u1',
        #price_id='pr1',
        name='Test Product',
        link='https://example.com/product',
        image_url='https://example.com/image.jpg',
        rating=4.5,
        categories='cat1, cat2'
    )

@pytest.fixture
def orm_product_integration():
    '''Фикстура тестового ORM Product с JSON-сериализованными категориями'''
    product = ORMProduct(
        id='p1',
        user_id='u1',
        #price_id='pr1',
        name='Test Product',
        link='https://example.com/product',
        image_url='https://example.com/image.jpg',
        rating=4.5,
        categories='cat1, cat2'
    )
    return product