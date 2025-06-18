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

@pytest.fixture
def price_parser(mock_adapter):
    adapters = {'ozon': mock_adapter}
    return PriceParser(adapters)

def test_parse_valid_marketplace(price_parser, mock_adapter):
    product = price_parser.parse('https://ozon.ru/product/1234456789', 'ozon')
    assert isinstance(product, Product)
    assert product.id == '1234456789'
    mock_adapter.parse_product.assert_called_once_with('https://ozon.ru/product/1234456789')

def test_parse_invalid_marketplace(price_parser):
    with pytest.raises(ValueError, match='Маркетплейс invalid не поддерживается'):
        price_parser.parse('https://ozon.ru/product/1234456789', 'invalid')