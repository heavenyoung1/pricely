import pytest
from pydantic import HttpUrl

from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct


@pytest.fixture
def product():
    '''Фикстура тестового доменного Product'''
    return Product(
        id='816992280',
        user_id='5702092394',
        name='Рюкзак мужской городской спортивный',
        link='https://www.ozon.ru/product/ryukzak-muzhskoy-gorodskoy-sportivnyy-tevin-816992280/',
        image_url='https://ir.ozone.ru/s3/multimedia-f/wc1000/6723691791.jpg',
        rating=4.9,
        categories='Аксессуары, Мужчинам, Сумки и рюкзаки, Рюкзаки, TEVIN'
    )

@pytest.fixture
def orm_product():
    '''Фикстура тестового ORMProduct'''
    return ORMProduct(
        id='816992280',
        name='Рюкзак мужской городской спортивный',
        link='https://www.ozon.ru/product/ryukzak-muzhskoy-gorodskoy-sportivnyy-tevin-816992280/',
        image_url='https://example.com/image.jpg',
        rating=4.9,
        categories='Аксессуары, Мужчинам, Сумки и рюкзаки, Рюкзаки, TEVIN'
    )

# @pytest.fixture
# def product_integration():
#     '''Фикстура тестового доменного Product'''
#     return Product(
#         id='p1',
#         user_id='u1',
#         name='Test Product',
#         link='https://example.com/product',
#         image_url='https://example.com/image.jpg',
#         rating=4.5,
#         categories='cat1, cat2'
#     )

# @pytest.fixture
# def orm_product_integration():
#     '''Фикстура тестового ORM Product'''
#     product = ORMProduct(
#         id='p1',
#         user_id='u1',
#         name='Test Product',
#         link='https://example.com/product',
#         image_url='https://example.com/image.jpg',
#         rating=4.5,
#         categories='cat1, cat2'
#     )
#     return product