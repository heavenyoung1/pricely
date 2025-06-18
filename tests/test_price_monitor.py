from unittest.mock import Mock, AsyncMock, patch
import pytest
from datetime import datetime

from core.price_monitor import PriceMonitor
from models.product import Product

@pytest.fixture
def mock_parser():
    """Create a mock parser returning a product with a fixed price."""
    parser = Mock()
    parser.parse_product.return_value = Product(
        id="1235456789",
        url="https://ozon.ru/product/1235456789",
        name="Test Product",
        price=900,  # Price set to 900 to simulate change
        last_updated=datetime(2025, 6, 16),
    )
    return parser

@pytest.fixture
def mock_cache():
    '''Create a mock cache with a fixed old price.'''
    cache = Mock()
    cache.get_price.return_value = 1000
    cache.save_price = Mock()
    return cache


@pytest.fixture
def mock_notifier():
    '''Create a mock notifier with an async notify method.'''
    notifier = Mock()
    notifier.notify = AsyncMock()
    return notifier


@pytest.fixture
def price_monitor(mock_parser, mock_cache, mock_notifier):
    '''Create a PriceMonitor instance with mocked dependencies.'''
    return PriceMonitor(
        parser=mock_parser,
        cache=mock_cache,
        notifier=mock_notifier,
        interval=1,
    )


@pytest.mark.asyncio
@patch("core.price_monitor.random.uniform", return_value=50)
@patch("core.price_monitor.time.sleep")
async def test_monitor_price_change(mock_sleep, mock_random, price_monitor):
    """Test that a price change triggers a notification and updates cache."""
    price_monitor.cache.get_price.side_effect = [1000, 1000]
    await price_monitor.check_once("https://ozon.ru/product/1235456789", chat_id=12345)
    price_monitor.notifier.notify.assert_called_once_with(
        chat_id=12345,
        product=price_monitor.parser.parse_product.return_value,
        old_price=1000,
    )
    price_monitor.cache.save_price.assert_called_with("https://ozon.ru/product/1235456789", 900)
    assert price_monitor.attempts.get("https://ozon.ru/product/123", 0) == 0


@pytest.mark.asyncio
@patch('core.price_monitor.time.sleep')
async def test_monitor_no_price_change(mock_sleep, price_monitor):
    '''Test that no notification is sent when price doesn't change.'''
    price_monitor.parser.parse_product.return_value.price = 1000  # Match cache price
    price_monitor.cache.get_price.return_value = 1000
    await price_monitor.check_once('https://ozon.ru/product/1235456789', chat_id=12345)
    price_monitor.notifier.notify.assert_not_called()
    price_monitor.cache.save_price.assert_called_with('https://ozon.ru/product/123', 1000)


@pytest.mark.asyncio
@patch('core.price_monitor.random.uniform', return_value=50)
@patch('core.price_monitor.time.sleep')
async def test_monitor_error(mock_sleep, mock_random, price_monitor):
    '''Test that an error increments attempts and doesn't notify.'''
    price_monitor.parser.parse_product.side_effect = Exception('Parse error')
    await price_monitor.check_once('https://ozon.ru/product/123', chat_id=12345)
    assert price_monitor.attempts.get('https://ozon.ru/product/123', 0) == 1
    price_monitor.notifier.notify.assert_not_called()