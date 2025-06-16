from datetime import datetime

import pytest

from models.product import Product


@pytest.fixture
def product():
    return Product(
        id='1234567890',
        url='https://ozon.ru/product/1234567890',
        name='Test Product',
        price=9999,
        last_updated=datetime(2025, 6, 16, 4, 20, 00)
    )