import pytest
from src.application.use_cases.get_full_product import GetFullProductUseCase
from src.domain.exceptions import ProductNotFoundError

def test_get_full_product_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    product,
    price,
    user,
    ):
    '''Тест успешного получения полной информации о товаре (продукт, цена, пользователь).'''
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get.return_value = price
    pure_mock_user_repo.get.return_value = user

    use_case = GetFullProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo
    )
    result = use_case.execute(product_id=product.id)
    # Проверяем результат
    assert result['product'] == product
    assert result['price'] == price
    assert result['user'] == user

    pure_mock_product_repo.get.assert_called_once_with(product.id)
    pure_mock_price_repo.get.assert_called_once_with(product.price_id)
    pure_mock_user_repo.get.assert_called_once_with(product.user_id)

def test_get_full_product_product_not_found(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo
):
    '''Тест ошибки когда продукт не найден.'''
    use_case = GetFullProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo
    )
    # Ожидаем исключение
    with pytest.raises(ProductNotFoundError, match='Товар NOT_EXIST_ID не существует'):
        use_case.execute(product_id='NOT_EXIST_ID')

    # Проверяем, что только product_repo был вызван
    pure_mock_product_repo.get.assert_called_once_with('NOT_EXIST_ID')
    pure_mock_price_repo.get.assert_not_called()
    pure_mock_user_repo.get.assert_not_called()