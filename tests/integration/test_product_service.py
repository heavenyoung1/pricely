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
def test_create_product_success(uow, user, pure_mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    # Создаем пользователя
    service.create_user(user)

    # Создаем продукт
    url = "https://ozon.ru/product/123"
    result = service.create_product(user.id, url)

    assert result["id"] == "p1"
    with uow:
        product = uow.product_repository.get("p1")
        assert product is not None
        assert product.price_id is not None

        price = uow.price_repository.get(product.price_id)
        assert price is not None
        assert price.with_card == 100
        assert price.without_card == 120
        assert price.default == 150