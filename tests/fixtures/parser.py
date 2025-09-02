import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_parser():
    parser = MagicMock()
    parser.parse_product.return_value = {
        'id': 'p1',
        'name':'Test Product',
        'image_url': 'https://example.com/image.jpg',
        'rating': 4.5,
        'categories': ['cat1', 'cat2'],
        'price_with_card': 100,
        'price_without_card': 120,
        'price_default': 150,
    }
    return parser