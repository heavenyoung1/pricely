import pytest
import logging
import json
import sys
from datetime import datetime
from pydantic import HttpUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.models import ORMProduct, ORMUser, ORMPrice
from src.interfaces.dto import ProductDTO, PriceDTO, UserDTO
from src.domain.entities import Product, Price, User

# ----- # ----- # ----- Общие настройки ----- # ----- # ----- #

@pytest.fixture(autouse=True)
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

@pytest.fixture
def session():
    '''Создает временную сессию SQLite в памяти для тестов.
    Автоматически создает таблицы и закрывает сессию после использования.'''
    engine = create_engine('sqlite:///:memory:')
    ORMUser.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close() 

# ----- # ----- # ----- Фикстуры DTO слоя ----- # ----- # ----- #

@pytest.fixture
def product_dto():
    '''Фикстура тестового Product DTO'''
    return ProductDTO(
        id='p1',
        user_id='u1',
        name='Test Product',
        link=HttpUrl('https://example.com/product'),
        image_url=HttpUrl('https://example.com/image.jpg'),
        rating=4.5,
        categories=['cat1', 'cat2']
    )

@pytest.fixture
def price_dto():
    '''Фикстура тестового Price DTO'''
    return PriceDTO(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        default=150,
        claim=datetime(2025, 1, 1)
    )

@pytest.fixture
def user_dto():
    '''Фикстура тестового User DTO'''
    return UserDTO(
        id='u1',
        username='test_user',
        chat_id='12345',
        products=['p1', 'p2']
    )

# ----- # ----- # ----- Фикстуры DOMAIN слоя ----- # ----- # ----- #

@pytest.fixture
def product():
    '''Фикстура тестового доменного Product'''
    return Product(
        id='p1',
        user_id='u1',
        price_id='pr1',
        name='Test Product',
        link='https://example.com/product',
        image_url='https://example.com/image.jpg',
        rating=4.5,
        categories=['cat1', 'cat2']
    )

@pytest.fixture
def price():
    '''Фикстура тестового доменного Price'''
    return Price(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        default=150,
        claim=datetime(2025, 1, 1)
    )

@pytest.fixture
def user():
    '''Фикстура тестового доменного User'''
    return User(
        id='u1',
        username='test_user',
        chat_id='12345',
        products=['p1', 'p2']
    )

# ----- # ----- # ----- Фикстуры ORM слоя ----- # ----- # ----- #

@pytest.fixture
def orm_product(session):
    '''Фикстура тестового ORM Product с JSON-сериализованными категориями'''
    product = ORMProduct(
        id='p1',
        user_id='u1',
        price_id='pr1',
        name='Test Product',
        link='https://example.com/product',
        image_url='https://example.com/image.jpg',
        rating=4.5,
        categories=json.dumps(['cat1', 'cat2'])  # Явная сериализация в JSON
    )
    session.add(product)
    session.commit()
    return product

@pytest.fixture
def orm_price(session):
    '''Фикстура тестового ORM Price'''
    price = ORMPrice(
        id='pr1',
        product_id='p1',
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        default=150,
        claim=datetime(2025, 1, 1)
    )
    session.add(price)
    session.commit()
    return price

@pytest.fixture
def orm_user(session):
    '''Фикстура тестового ORM User'''
    user = ORMUser(
        id='u1',
        username='test_user',
        chat_id='12345',
        products=['p1', 'p2']
    )
    session.add(user)
    session.commit()
    return user