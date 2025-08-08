import pytest
from datetime import datetime
from pydantic import HttpUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.models import ORMProduct, ORMUser, ORMPrice
from src.domain.entities import Product, Price, User

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

@pytest.fixture
def product():
    '''Фикстура тестового продукта с минимальными обязательными полями:
    - id: тестовый идентификатор товара
    - user_id: привязка к пользователю
    - name: название товара
    - link: валидный URL товара
    - image_url: валидный URL изображения
    - rating: рейтинг товара
    - categories: список категорий'''
    return Product(
        id='01234567521',
        user_id='user1',
        price_id='price1',
        name='Test Product',
        link=HttpUrl('http://example.com'),
        image_url=HttpUrl('http://example.com/image.jpg'),
        rating=4.5,
        categories=['electronics', 'gadgets']
    )

@pytest.fixture
def price():
    '''Фикстура тестовой цены с параметрами:
    - id: идентификатор ценового снимка
    - product_id: привязка к продукту
    - with_card/without_card: текущие цены
    - previous_*: предыдущие цены (опционально)
    - default: цена по умолчанию
    - claim: метка времени фиксации цены'''
    return Price(
        id='price1',
        product_id='prod1',
        with_card=100,
        without_card=120,
        previous_with_card=None,
        previous_without_card=None,
        default=0,
        claim=datetime(2023, 1, 1)
    )

@pytest.fixture
def user():
    '''Фикстура тестового пользователя с полями:
    - user_id: уникальный идентификатор
    - username: имя пользователя
    - chat_id: идентификатор чата
    - products: JSON-строка со списком ID товаров'''
    return User(
        user_id='user1',
        username='test_user',
        chat_id='123456',
        products='["prod1"]'  # JSON с ID продуктов
    )