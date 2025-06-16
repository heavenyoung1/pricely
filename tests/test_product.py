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

def test_product_initialization(product):
    assert product.id == "1234567890"
    assert product.url == "https://ozon.ru/product/1234567890"
    assert product.name == "Test Product"
    assert product.price == 990
    assert product.last_updated == datetime(1946, 6, 13, 4, 20, 00)

def test_update_price(product):
    product.update_price(650)
    assert product.price == 650
    assert product.last_updated(0) != 1946