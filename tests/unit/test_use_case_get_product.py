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
        mocker,
):
    '''Успешное получение товара.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=product)

    # Создаем use case
    use_case = GetProductUseCase(product_repo=mock_product_repo)

    # Выполняем
    result = use_case.execute(product_id=product.id)

    # Проверяем результат и вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    assert result == product
    mock_product_repo.get.assert_called_once_with(product.id)

def test_get_product_use_case_not_found(
        mock_product_repo,
        mocker,
):
    '''Проверяет, что выбрасывается ProductNotFoundError, если продукт не существует.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=None)

    # Создаем use case
    use_case = GetProductUseCase(product_repo=mock_product_repo)

    # Проверяем, что выбрасывается ProductNotFoundError
    with pytest.raises(ProductNotFoundError, match='Продукт ID_ID не существует'):
        use_case.execute(product_id='ID_ID')

    # Проверяем вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    mock_product_repo.get.assert_called_once_with('ID_ID')

def test_get_product_use_case_empty_product_id(
        mock_product_repo,
        mocker,
):
    '''Проверяет, что выбрасывается ProductNotFoundError, если product_id пустой.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=None)

    # Создаем use case
    use_case = GetProductUseCase(product_repo=mock_product_repo)

    # Проверяем, что выбрасывается ProductNotFoundError
    with pytest.raises(ProductNotFoundError, match='Идентификатор продукта не указан'):
        use_case.execute(product_id='')

    # Проверяем, что get не вызывался
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    mock_product_repo.get.assert_not_called()