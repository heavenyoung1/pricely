import logging
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.infrastructure.database.models.base import Base
from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp
from src.infrastructure.database.models.product import DBProduct
from src.infrastructure.database.models.price_stamp import DBPriceStamp
from src.infrastructure.repositories.pg_product_repository import PGSQLProductRepository


def pytest_configure(config):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

@pytest.fixture
def product_test():
    return {
        'product_id': '1804652778',  # Было 'id'
        'user_id': '0000000000',
        'name': 'Чаша для кальяна глиняная',
        'rating': 4.9,
        'price_with_card': 500,
        'price_without_card': 561,
        'previous_price_with_card': 600,
        'previous_price_without_card': 600,
        'price_default': 899,
        # 'discount_amount': float,
        'link': 'https://www.ozon.ru/product/chasha-dlya-kalyana-glinyanaya-cosmo-bowl-turkish-shot-1804652778/',
        'url_image': 'https://ir.ozone.ru/s3/multimedia-1-9/wc1000/7352613513.jpg',
        'category_product': [
            'Товары для курения и аксессуары',
            'Товары для курения',
            'Аксессуары и комплектующие для кальянов',
            'Комплектующие',
            'Cosmo Bowl',
        ],
        'last_timestamp': datetime(2025, 1, 1, 1, 2, 3),  # Было 'timestamp'
    }


def product(product_test):
    return Product(**product_test)

@pytest.fixture
def price_stamp():
    return PriceStamp(
        ID_stamp='stamp1',  # Использую str, чтобы соответствовать DBPriceStamp
        ID_product='1804652778',
        time_stamp=datetime(2025, 1, 1, 1, 2, 3),
        price_with_card=500,
        price_without_card=561,
        previous_price_with_card=600,
        previous_price_without_card=600,
        price_default=899,
    )

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.rollback()
    Base.metadata.drop_all(engine)
    session.close()

@pytest.fixture
def repo(db_session):
    return PGSQLProductRepository(db_session)