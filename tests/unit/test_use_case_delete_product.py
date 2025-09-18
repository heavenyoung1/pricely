import pytest

from src.application.use_cases.delete_product import DeleteProductUseCase
from src.domain.exceptions import ProductNotExistingDataBase


@pytest.mark.unit
def test_delete_product_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    product,
    price,
    user,
):
    # Настраиваем моки
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get_all_prices_by_product.return_value = [price]
    pure_mock_user_repo.get.return_value = user

    use_case = DeleteProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    use_case.execute(product_id=product.id)

    # Проверяем вызовы
    pure_mock_price_repo.delete.assert_called_once_with(price.id)
    pure_mock_product_repo.delete.assert_called_once_with(product.id)
    pure_mock_user_repo.save.assert_called_once()
    assert product.id not in user.products

@pytest.mark.unit
def test_delete_product_use_case_unsuccess_notexist_in_db(
    pure_mock_product_repo,
    pure_mock_price_repo,
    pure_mock_user_repo,
    product,
):
    pure_mock_product_repo.get.return_value = None

    use_case = DeleteProductUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
        user_repo=pure_mock_user_repo,
    )

    with pytest.raises(ProductNotExistingDataBase, match=f'Товар {product.id} не существует в БД!'):
        use_case.execute(product_id=product.id)


