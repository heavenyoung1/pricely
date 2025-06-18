import pytest
from unittest.mock import Mock, patch

from adapters.wb_adapter import WBAdapter
from models.product import Product
from datetime import datetime

@pytest.fixture
def wb_adapter():
    with patch('adapters.wb_adapter.webdriver.Chrome') as mock_chrome:
        adapter = WBAdapter(driver_path='chromedriver')
        adapter.driver = Mock()
        yield adapter

def test_get_id():
    url = 'https://www.wildberries.ru/catalog/1236667890/detail.aspx'
    assert WBAdapter._get_id(url) == '1236667890'

def test_parse_product(wb_adapter):
    mock_driver = wb_adapter.driver
    mock_driver.find_element.side_effect = [
        Mock(text='Test Product'),
        Mock(text=450),
    ]

    product = wb_adapter.parse_product('https://www.wildberries.ru/catalog/1234577890/detail.aspx')
    assert isinstance(product, Product)
    assert product.id == '1234577890'
    assert product.name == 'Test Product'
    assert product.price == 450
    assert product.url == 'https://www.wildberries.ru/catalog/1234577890/detail.aspx'
    assert isinstance(product.last_updated, datetime)

def test_parse_product_error(wb_adapter):
    wb_adapter.driver.find_element.side_effect = Exception('Element not found')
    with pytest.raises(ValueError, match="Ошибка парсинга Wildberries"):
        wb_adapter.parse_product("https://wildberries.ru/catalog/123")