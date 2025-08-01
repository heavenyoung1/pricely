import pytest
from datetime import datetime

@pytest.fixture
def product_test():
    return {
        'product_id': '1804652778',  # Было 'id'
        'user_id': '0000000000',
        'name': 'Чаша для кальяна глиняная',
        'rating': 4.9,
        'price_with_card': 500,
        'price_without_card': 561,
        'previous_price_with_card': 600,
        'previous_price_without_card': 600,
        'price_default': 899,
        # 'discount_amount': float,
        'link': 'https://www.ozon.ru/product/chasha-dlya-kalyana-glinyanaya-cosmo-bowl-turkish-shot-1804652778/',
        'url_image': 'https://ir.ozone.ru/s3/multimedia-1-9/wc1000/7352613513.jpg',
        'category_product': [
            'Товары для курения и аксессуары',
            'Товары для курения',
            'Аксессуары и комплектующие для кальянов',
            'Комплектующие',
            'Cosmo Bowl',
        ],
        'last_timestamp': datetime(2025, 1, 1, 1, 2, 3),  # Было 'timestamp'
    }