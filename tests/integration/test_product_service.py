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
    mock_parser.parse_product.return_value = {
        "id": "p_new",  # ⚠️ новый ID, чтобы не пересекаться с существующими
        "name": "Test Product",
        "image_url": "https://example.com/image.jpg",
        "rating": 4.5,
        "categories": ["cat1", "cat2"],
        "price_with_card": 100,
        "price_without_card": 120,
        "price_default": 150,
    }

    service = ProductService(uow_factory=lambda: uow, parser=mock_parser)

    # Создаём пользователя
    service.create_user(user)

    # Создаём продукт
    url = "https://ozon.ru/product/123"
    result = service.create_product(user.id, url)

    # Проверяем результат
    assert result["product_id"] == "p_new"
    assert result["product_name"] == "Test Product"
    assert result["user_id"] == user.id

    # Проверяем, что в БД всё сохранилось
    with uow:
        saved_product = uow.product_repository.get("p_new")
        assert saved_product is not None
        assert saved_product.price_id is not None

        saved_price = uow.price_repository.get(saved_product.price_id)
        assert saved_price is not None
        assert saved_price.product_id == saved_product.id