import pytest

from src.application.use_cases.get_product import GetProductUseCase
from src.domain.exceptions import ProductNotFoundError


@pytest.mark.unit
def test_get_product_use_case_success(
    pure_mock_product_repo,
    product,
):
    # Настраиваем мок
    pure_mock_product_repo.get.return_value = product

    use_case = GetProductUseCase(
        product_repo=pure_mock_product_repo,
    )
    use_case.execute(product_id=product.id)

    pure_mock_product_repo.get.assert_called_once_with(product.id)


@pytest.mark.unit
def test_get_product_use_case_unsuccess_not_found(
    pure_mock_product_repo,
    product,
):
    # Мок не настраиваем, в фикстуре уже None

    use_case = GetProductUseCase(
        product_repo=pure_mock_product_repo,
    )
    with pytest.raises(
        ProductNotFoundError, match=f"Продукт {product.id} не существует"
    ):
        use_case.execute(product_id=product.id)

    pure_mock_product_repo.get.assert_called_once_with(product.id)


@pytest.mark.unit
def test_get_product_use_case_unsuccess_empty_product_id(
    pure_mock_product_repo,
):
    # Мок не настраиваем, в фикстуре уже None

    use_case = GetProductUseCase(
        product_repo=pure_mock_product_repo,
    )
    with pytest.raises(ProductNotFoundError, match=f"Идентификатор продукта не указан"):
        use_case.execute(product_id=None)

    # pure_mock_product_repo.get.assert_called_once_with(product.id)
