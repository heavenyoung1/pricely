import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def mock_parser(mocker):
    return mocker.Mock()


@pytest.fixture
def parser_data(product, price_created_first):
    """Фикстура с данными, которые возвращает парсер"""
    return {
        "id": product.id,
        "name": product.name,
        "rating": product.rating,
        "price_with_card": price_created_first.with_card,
        "price_without_card": price_created_first.without_card,
        "image_url": product.image_url,
        "categories": product.categories,
    }


@pytest.fixture
def pure_mock_parser():
    """Чистый мок для ProductParser."""
    mock = Mock()
    mock.parse_product.return_value = {
        "id": "816992280",
        "name": "Рюкзак мужской городской спортивный",
        "image_url": "https://ir.ozone.ru/s3/multimedia-f/wc1000/6723691791.jpg",
        "rating": 4.9,
        "categories": ["Аксессуары", "Мужчинам", "Сумки и рюкзаки", "Рюкзаки", "TEVIN"],
        "price_with_card": 1676,
        "price_without_card": 1827,
    }
    return mock
