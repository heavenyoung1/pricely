import pytest

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