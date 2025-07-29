from datetime import datetime
from unittest.mock import Mock
import logging

from src.application.services.product_service import ProductService
from tests.fixtures.product import product_test

logger = logging.getLogger(__name__)

def test_success_create_product(product_test):
    '''TEST - SUCCESSED CREATED PRODUCT'''
    # Arrange
    repository = Mock()
    service = ProductService(repository)

    # Action
    product = service.create_product(**product_test)

    #Assert of main data types 
    assert len(product.id) == 10
    assert isinstance(product.price_default, int)
    assert isinstance(product.price_without_card, int)
    assert isinstance(product.price_default, int)
    assert isinstance(product.link, str)
    assert isinstance(product.category_product, list)
    assert isinstance(product.timestamp, datetime)

    # Assert main of product data
    assert product.id == '1804652778'
    assert product.name == 'Чаша для кальяна глиняная'
    assert product.price_with_card == 500
    assert product.price_without_card == 561
    assert product.price_default == 899
    assert product.link.startswith('https://')
    assert product.url_image.endswith(('.jpg', '.jpeg', '.png'))
    assert len(product.category_product) > 0
    assert product.timestamp == datetime(2025, 1, 1, 1, 2, 3)
    logger.info(f'Successfully created product: {product.id}')




    
