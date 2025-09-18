import pytest
from src.infrastructure.services import ProductService
from src.domain.entities import User, Product, Price
from src.domain.exceptions import (
    ProductNotFoundError, PriceUpdateError, ProductCreationError,
    UserCreationError, ParserProductError, ProductDeletingError, ProductNotExistingDataBase
)

# ==================== GET PRODUCT ====================

@pytest.mark.integration
def test_get_product_success(uow, product, user, pure_mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    # Создаём данные
    service.create_user(user)
    service.create_product(user.id, "https://ozon.ru/product/123")
    with uow:
        product = service.get_product(product_id=product.id)
        assert product is not None
        assert product.id == 'p1'
        assert product.name == product.name

def test_get_product_not_found(uow, pure_mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    with pytest.raises(ProductNotFoundError):
        service.get_product(product_id="NOT_EXIST")

# ==================== GET FULL PRODUCT ====================

@pytest.mark.integration
def test_get_full_product_success(uow, product, user, pure_mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    # создаём данные
    service.create_user(user)
    service.create_product(user.id, "https://ozon.ru/product/123")

    with uow:
        full_product = service.get_full_product(product_id=product.id)
        assert full_product['id'] == product.id
        assert 'prices' in full_product
        # Вот тут нужно переделать, у меня ведь другая архитектура (есть таблица user_products)
        #assert full_product['user']['id'] == user.id


@pytest.mark.integration
def test_get_full_product_not_found(uow, pure_mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    with pytest.raises(ProductNotFoundError):
        service.get_full_product(product_id="NOT_EXIST")

# ==================== CREATE USER ====================

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

# ==================== CREATE PRODUCT ====================

@pytest.mark.integration
def test_create_product_success(uow, user, pure_mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    service.create_user(user)

    url = "https://ozon.ru/product/123"
    result = service.create_product(user.id, url)

    assert result["product_id"] == "p1"

    with uow:
        product = uow.product_repository.get("p1")
        assert product is not None
        assert result["with_card"] == 100

# ==================== DELETE PRODUCT ====================

@pytest.mark.integration
def test_delete_product_success(uow, product , user, pure_mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    service.create_user(user)
    service.create_product(user.id, "https://ozon.ru/product/123")

    service.delete_product(product_id=product.id)

    with uow:
        product_uow = uow.product_repository.get(product_id=product.id)
        assert product_uow is None

@pytest.mark.integration
def test_delete_product_not_found(uow, pure_mock_parser):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    with pytest.raises(ProductNotExistingDataBase):
        service.delete_product(product_id="NOT_EXIST")

# ==================== UPDATE PRICE ====================

@pytest.mark.integration
def test_update_product_price(uow, product, user, pure_mock_parser, price, price_second):
    service = ProductService(uow_factory=lambda: uow, parser=pure_mock_parser)

    service.create_user(user)
    result = service.create_product(user.id, "https://ozon.ru/product/123")

    service.update_product_price(product_id=product.id, price=price_second)

    with uow:
            product_with_upd_price = uow.product_repository.get(product_id=result["product_id"])
            assert product_with_upd_price is not None