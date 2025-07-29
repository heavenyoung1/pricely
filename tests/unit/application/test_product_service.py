from datetime import datetime
from unittest.mock import Mock
import pytest

from src.application.services.product_service import ProductService
from src.domain.entities.product import Product

@pytest.fixture
def product_test():
    return {
            'id' :'1804652778',
            'name': 'Чаша для кальяна глиняная',
            'rating': 4.9,
            'price_with_card': 500,
            'price_without_card': 561,
            #previous_price_without_card: int
            'price_default': 899,
            #discount_amount: float
            'link': 'https://www.ozon.ru/product/chasha-dlya-kalyana-glinyanaya-cosmo-bowl-turkish-shot-1804652778/',
            'url_image': 'https://ir.ozone.ru/s3/multimedia-1-9/wc1000/7352613513.jpg',
            'category_product': [
                'Товары для курения и аксессуары',
                'Товары для курения',
                'Аксессуары и комплектующие для кальянов',
                'Комплектующие',
                'Cosmo Bowl',
                ],
            'timestamp': datetime(2025, 1, 1, 1, 2, 3),
    }


def test_success_create_product(product_test):
    repository = Mock()
    service = ProductService(repository)
    product = service.create_product(**product_test)
    assert product.id == '1804652778'
    
