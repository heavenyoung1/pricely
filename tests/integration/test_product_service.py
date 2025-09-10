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

    service.create_user(user)

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













































# import pytest
# from datetime import datetime
# from src.domain.entities import User, Price


# # ==================== USER TESTS ====================

# @pytest.mark.integration
# def test_create_and_get_user(uow, user, pure_mock_parser):
#     service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

#     # Создаем пользователя
#     service.create_user(user)

#     with uow:
#         saved = uow.user_repository.get(user.id)
#         assert saved is not None
#         assert saved.username == user.username
#         assert saved.chat_id == user.chat_id


# # ==================== PRODUCT CREATION ====================

# @pytest.mark.integration
# def test_create_product_success(uow, user, pure_mock_parser):
#     service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

#     # Создаем пользователя
#     service.create_user(user)

#     # Создаем продукт
#     url = "https://ozon.ru/product/123"
#     result = service.create_product(user.id, url)

#     assert result["id"] == "p1"
#     with uow:
#         product = uow.product_repository.get("p1")
#         assert product is not None
#         assert product.price_id is not None

#         price = uow.price_repository.get(product.price_id)
#         assert price is not None
#         assert price.with_card == 100
#         assert price.without_card == 120
#         assert price.default == 150


# # ==================== GET PRODUCT ====================

# @pytest.mark.integration
# def test_get_product_and_full_product(uow, user, pure_mock_parser):
#     service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)
#     service.create_user(user)
#     service.create_product(user.id, "https://ozon.ru/product/123")

#     product = service.get_product("p1")
#     assert product.id == "p1"

#     full = service.get_full_product("p1")
#     assert full["product"].id == "p1"
#     assert full["price"].with_card == 100
#     assert full["user"].id == user.id


# # ==================== UPDATE PRICE ====================

# @pytest.mark.integration
# def test_update_product_price(uow, user, pure_mock_parser):
#     service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)
#     service.create_user(user)
#     service.create_product(user.id, "https://ozon.ru/product/123")

#     new_price = Price(
#         id="price2",
#         product_id="p1",
#         with_card=200,
#         without_card=220,
#         previous_with_card=100,
#         previous_without_card=120,
#         default=250,
#         claim=datetime.now()
#     )

#     service.update_product_price("p1", new_price)

#     with uow:
#         product = uow.product_repository.get("p1")
#         assert product.price_id == "price2"

#         updated_price = uow.price_repository.get("price2")
#         assert updated_price.with_card == 200
#         assert updated_price.previous_with_card == 100


# # ==================== DELETE PRODUCT ====================

# @pytest.mark.integration
# def test_delete_product(uow, user, pure_mock_parser):
#     service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)
#     service.create_user(user)
#     service.create_product(user.id, "https://ozon.ru/product/123")

#     service.delete_product("p1")

#     with uow:
#         assert uow.product_repository.get("p1") is None
#         prices = uow.price_repository.list_by_product("p1")
#         assert prices == []