import pytest
from datetime import datetime
from pydantic import HttpUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.models import ORMProduct, ORMUser, ORMPrice
from src.domain.entities import Product, Price, User

@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    ORMUser.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close() 

@pytest.fixture
def product():
    return Product(
        id='01234567521',
        user_id='user1',
        price_id=None,
        name='Test Product',
        link=HttpUrl('http://example.com'),
        image_url=HttpUrl('http://example.com/image.jpg'),
        rating=4.5,
        categories=['electronics', 'gadgets']
    )

@pytest.fixture
def price():
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
    return User(
        user_id="user1",
        username="test_user",
        chat_id="123456",
        products='["prod1"]'  # JSON с ID продуктов
    )