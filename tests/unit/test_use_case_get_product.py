import pytest
import json
from src.application.use_cases.get_product import GetProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.database.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
from src.domain.exceptions import ProductNotFoundError

def test_get_product_use_case_success(
    pure_mock_product_repo,
    product,
):
    # Настраиваем мок
    pure_mock_product_repo.get.return_value = product

    use_case = GetProductUseCase(
        product_repo=pure_mock_product_repo,
    )
    result = use_case.execute(product_id=product.id)

    pure_mock_product_repo.get.assert_called_once_with(product.id)

def test_get_product_use_case_unsuccess_not_found(
    pure_mock_product_repo,
    product,
):
    # Мок не настраиваем, в фикстуре уже None

    use_case = GetProductUseCase(
        product_repo=pure_mock_product_repo,
    )
    with pytest.raises(ProductNotFoundError, match=f'Продукт {product.id} не существует'):
        use_case.execute(product_id=product.id)
    
    pure_mock_product_repo.get.assert_called_once_with(product.id)