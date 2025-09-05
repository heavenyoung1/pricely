import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_parser(mocker):
    return mocker.Mock()

@pytest.fixture
def parser_data(product, price):
    '''Фикстура с данными, которые возвращает парсер'''
    return {
        'id': product.id,
        'name': product.name,
        'rating': product.rating,
        'price_with_card': price.with_card,
        'price_without_card': price.without_card,
        'price_default': price.default,
        'image_url': product.image_url,
        'categories': product.categories,
    }

@pytest.fixture
def pure_mock_parser():
    '''Чистый мок для ProductParser.'''
    mock = Mock()
    mock.parse_product.return_value = {
        'id': 'p1',
        'name': 'Test Product',
        'image_url': 'https://example.com/image.jpg',
        'rating': 4.5,
        'categories': ['cat1', 'cat2'],
        'price_with_card': 100,
        'price_without_card': 120,
        'price_default': 150,
    }
    return mock