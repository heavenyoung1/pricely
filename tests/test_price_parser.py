import pytest
from unittest.mock import Mock

from core.price_parser import PriceParser
from models.product import Product
from datetime import datetime

@pytest.fixture
def mock_adapter():
    adapter = Mock()
    adapter.parse_product.return_value = Product(
        id='1234456789',
        url='https://ozon.ru/product/1234456789',
        name='Test Product',
        price=1000,
        last_updated=datetime(2025, 6, 16)  
    )
    return adapter


