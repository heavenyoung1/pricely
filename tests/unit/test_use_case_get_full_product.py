import pytest
from src.application.use_cases.get_full_product import GetFullProductUseCase
from src.domain.exceptions import ProductNotFoundError

@pytest.mark.unit
def test_get_full_product_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    product,
    price,
    user,
):
    '''Тест успешного получения полной информации о товаре (продукт, цены, пользователь).'''
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get_all_by_product.return_value = [price]
    pure_mock_user_repo.get.return_value = user

    use_case = GetFullProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    result = use_case.execute(product_id=product.id)

    assert result["id"] == product.id
    assert result["name"] == product.name
    assert len(result["prices"]) == 1
    assert result["prices"][0]["with_card"] == price.with_card
    assert result["user"]["id"] == user.id


@pytest.mark.unit
def test_get_full_product_product_not_found(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
):
    '''Тест ошибки когда продукт не найден.'''
    pure_mock_product_repo.get.return_value = None

    use_case = GetFullProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    with pytest.raises(ProductNotFoundError, match='Продукт NOT_EXIST_ID не найден'):
        use_case.execute(product_id='NOT_EXIST_ID')

    pure_mock_product_repo.get.assert_called_once_with('NOT_EXIST_ID')
    pure_mock_price_repo.get_all_by_product.assert_not_called()
    pure_mock_user_repo.get.assert_not_called()