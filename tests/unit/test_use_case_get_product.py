import pytest
import json
from src.application.use_cases.get_product import GetProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
from src.application.exceptions import ProductNotFoundError

def test_get_product_use_case_success(
        mock_product_repo, 
        product, 
    ):
    '''Успешное получение товара.'''

    # Настраиваем моки: продукт существует
    mock_product_repo.get.return_value = product

    # Создаём use case
    use_case = GetProductUseCase(product_repo=mock_product_repo)

    result = use_case.execute(product_id=product.id)

    # Проверяем, что репозиторий вызван
    mock_product_repo.get.assert_called_once_with(product.id)

    # Проверяем, что вернулся именно продукт
    assert result == product

def test_get_product_use_case_not_found(mock_product_repo):
    '''Возврат None, если товара нет.'''

    mock_product_repo.get.return_value = None
    use_case = GetProductUseCase(product_repo=mock_product_repo)

    # Выполняем получение продукта
    with pytest.raises(ProductNotFoundError, match=f'Продукт ID_ID не существует'):
        use_case.execute(product_id='ID_ID')

    # Выполняем получение продукта
    with pytest.raises(ProductNotFoundError, match=f'Идентификатор продукта не указан'):
        use_case.execute(product_id='')