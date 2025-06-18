from unittest.mock import Mock, AsyncMock, patch
import pytest
from datetime import datetime

from core.price_monitor import PriceMonitor
from models.product import Product

@pytest.fixture
def mock_parser():
    parser = Mock()
    parser.parse_product.return_value = Product(
        id='1234456789',
        url='https://ozon.ru/product/1235456789',
        name='Test Product',
        price=1000,
        last_updated=datetime(2025, 6, 16)  
    )
    return parser


@pytest.fixture
def mock_cache():
    cache = Mock()
    cache.get_price.return_value = 1000
    cache.save_price = Mock()
    return cache

@pytest.fixture
def mock_notifier():
    notifier = Mock()
    notifier.notify = AsyncMock()
    return notifier

@pytest.fixture
def price_monitor(mock_parser, mock_cache, mock_notifier):
    return PriceMonitor(parser=mock_parser, cache=mock_cache, notifier=mock_notifier, interval=1)
