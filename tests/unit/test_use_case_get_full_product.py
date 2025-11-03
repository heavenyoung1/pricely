import pytest
from src.application.use_cases.get_full_product import GetFullProductUseCase
from src.domain.exceptions import ProductNotFoundError


@pytest.mark.unit
def test_get_full_product_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    product,
    price_created_first,
    price_after_checking,
    user,
):
    """Тест успешного получения полной информации о товаре (продукт, цены, пользователь)."""
    pure_mock_product_repo.get.return_value = product
    # pure_mock_price_repo.get_all_prices_by_product.return_value = [price_created_first, price_after_checking]
    pure_mock_price_repo.get_latest_for_product.return_value = (
        price_after_checking  # Возвращаем нужный объект
    )
    pure_mock_user_repo.get.return_value = user

    use_case = GetFullProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    result = use_case.execute(product_id=product.id)

    assert result["id"] == product.id
    assert result["name"] == product.name
    assert result["latest_price"]["with_card"] == price_after_checking.with_card
    assert result["latest_price"]["without_card"] == price_after_checking.without_card
    assert (
        result["latest_price"]["previous_price_with_card"]
        == price_after_checking.previous_with_card
    )
    assert (
        result["latest_price"]["previous_price_without_card"]
        == price_after_checking.previous_without_card
    )


@pytest.mark.unit
def test_get_full_product_product_not_found(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
):
    """Тест ошибки когда продукт не найден."""
    pure_mock_product_repo.get.return_value = None

    use_case = GetFullProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    with pytest.raises(ProductNotFoundError, match="Продукт NOT_EXIST_ID не найден"):
        use_case.execute(product_id="NOT_EXIST_ID")

    pure_mock_product_repo.get.assert_called_once_with("NOT_EXIST_ID")
    pure_mock_price_repo.get_all_prices_by_product.assert_not_called()
    pure_mock_user_repo.get.assert_not_called()
