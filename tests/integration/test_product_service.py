import pytest
from src.infrastructure.services import ProductService
from src.domain.entities import User, Product, Price
from src.domain.exceptions import (
    ProductNotFoundError, PriceUpdateError, ProductCreationError,
    UserCreationError, ParserProductError, ProductDeletingError
)

# ==================== CREATE USER TESTS ====================

@pytest.mark.integration
def test_create_and_get_user(uow, user, mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=mock_parser)
    # Выполняем операцию
    service.create_user(user)
    with uow:
        saved_user = uow.user_repository.get(user.id)
        assert saved_user is not None
        assert saved_user.id == user.id
        assert saved_user.username == user.username
        assert saved_user.chat_id == user.chat_id

# ==================== CREATE PRODUCT TESTS ====================

@pytest.mark.integration
def test_create_product_success(uow, user, mock_parser):
    """Тест успешного создания продукта"""
    # Настраиваем мок парсера
    mock_parser.parse_product.return_value = {
        'id': 'p1',
        'name': 'Test Product',
        'image_url': 'https://example.com/image.jpg',
        'rating': 4.5,
        'categories': ['cat1', 'cat2'],
        'price_with_card': 100,
        'price_without_card': 120,
        'price_default': 150,
    }
    service = ProductService(uow_factory=lambda: uow, parser=mock_parser)

    # Создаем пользователя сначала
    service.create_user(user)

    # Создаем продукт
    url = 'https://ozon.ru/product/123'
    result = service.create_product(user.id, url, uow)