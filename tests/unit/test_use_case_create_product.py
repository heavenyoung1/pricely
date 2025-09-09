import pytest
import logging

from src.application.use_cases.create_product import CreateProductUseCase
from src.domain.exceptions import ProductCreationError


logger = logging.getLogger(__name__)

@pytest.mark.unit
def test_create_product_success_new_user(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_parser,
    user,
):
    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
    )

    result = use_case.execute(user_id=user.id, url="https://example.com/product")
    logger.debug(f"RESULT USE CASE -> {result}")

    assert result["product_id"] == "p1"
    assert result["product_name"] == "Test Product"
    assert result["user_id"] == "u1"

    # Проверяем вызовы
    pure_mock_parser.parse_product.assert_called_once_with("https://example.com/product")
    pure_mock_user_repo.get.assert_called_once_with("u1")
    pure_mock_product_repo.get.assert_called_once_with("p1")

    # user сохраняется 2 раза (создание + обновление списка продуктов)
    assert pure_mock_user_repo.save.call_count == 2
    # product сохраняется 2 раза (до и после установки price_id)
    assert pure_mock_product_repo.save.call_count == 2
    # price сохраняется 1 раз
    pure_mock_price_repo.save.assert_called_once()


@pytest.mark.unit
def test_create_product_success_existing_user(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_parser,
    user,
):
    pure_mock_user_repo.get.return_value = user

    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
    )

    result = use_case.execute(user_id=user.id, url="https://example.com/product")

    assert result["user_id"] == user.id

    # user сохраняется только 1 раз (обновление списка продуктов)
    assert pure_mock_user_repo.save.call_count == 1
    # product — 2 раза (до и после установки price_id)
    assert pure_mock_product_repo.save.call_count == 2
    # price — 1 раз
    pure_mock_price_repo.save.assert_called_once()


@pytest.mark.unit
def test_create_product_fails_product_exists(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    pure_mock_parser,
    product,
):
    """Тест: товар уже существует"""
    pure_mock_product_repo.get.return_value = product

    use_case = CreateProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
        parser=pure_mock_parser,
    )

    with pytest.raises(ProductCreationError, match="уже существует"):
        use_case.execute(user_id="u1", url="https://example.com/product")

    pure_mock_product_repo.save.assert_not_called()
    pure_mock_price_repo.save.assert_not_called()