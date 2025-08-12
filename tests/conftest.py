import pytest
import logging
import sys
from datetime import datetime
from pydantic import HttpUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.models import ORMProduct, ORMUser, ORMPrice
from src.domain.entities import Product, Price, User

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
        id='1509058661',
        user_id='515032006',
        price_id='1',
        name='Кофе молотый DeLonghi',
        link='https://www.ozon.ru/product/kofe-molotyy-delonghi-ground-selection-blend-250g-1509058661/?at=XQtkVkGBKc9WVJm3FygvwZkCxvwByoTrX0ZDZsggNYvE',
        image_url='https://ir.ozone.ru/s3/multimedia-1-f/wc1000/7413709479.jpg',
        rating=4.9,
        categories=['Продукты питания', 'Чай, кофе и какао', 'Кофе', 'Молотый', 'Delonghi']
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
        id='1',
        product_id='1509058661',
        with_card=582,
        without_card=629,
        previous_with_card=582,
        previous_without_card=629,
        default=1394,
        claim=datetime(2025, 1, 1),
    )

@pytest.fixture
def user():
    '''Фикстура тестового пользователя с полями:
    - id: уникальный идентификатор
    - username: имя пользователя
    - chat_id: идентификатор чата
    - products: JSON-строка со списком ID товаров'''
    return User(
        id='515032006',
        username='heavenyoung',
        chat_id='123456',
        products=[]  # Пустой список для нового продукта
    )