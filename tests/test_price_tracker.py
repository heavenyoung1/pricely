from unittest.mock import Mock, patch
import pytest
from core.price_tracker import PriceTracker
from models.product import Product
from datetime import datetime

@pytest.fixture
def mock_parser():
    """Create a mock parser returning a product with a fixed price."""
    parser = Mock()
    parser.parse.return_value = Product(
        id="123",
        url="https://ozon.ru/product/123",
        name="Test Product",
        price=1000,
        last_updated=datetime(2025, 6, 16)
    )
    return parser


@pytest.fixture
def mock_monitor():
    """Create a mock monitor with a cache."""
    monitor = Mock()
    monitor.cache = Mock()
    monitor.cache.save_price = Mock()
    return monitor


@pytest.fixture
def price_tracker(mock_parser, mock_monitor):
    """Create a PriceTracker instance with mocked dependencies."""
    with patch("core.price_parser.PriceParser", return_value=mock_parser):
        with patch("core.price_monitor.PriceMonitor", return_value=mock_monitor):
            return PriceTracker(
                driver_path="chromedriver",
                cache_file="prices.json",
                interval=3600
            )


def test_add_product(price_tracker, mock_parser, mock_monitor):
    """Test adding a product and saving its price to cache."""
    product = price_tracker.add_product(url="https://ozon.ru/product/123", marketplace="ozon")
    mock_parser.parse.assert_called_once_with("https://ozon.ru/product/123", "ozon")
    mock_monitor.cache.save_price.assert_called_once_with("https://ozon.ru/product/123", 1000)
    assert isinstance(product, Product)
    assert product.id == "123"


def test_monitor_price(price_tracker, mock_monitor):
    """Test initiating price monitoring for a product."""
    price_tracker.monitor_price(url="https://ozon.ru/product/123", chat_id=12345, marketplace="ozon")
    mock_monitor.monitor.assert_called_once_with("https://ozon.ru/product/123", 12345)