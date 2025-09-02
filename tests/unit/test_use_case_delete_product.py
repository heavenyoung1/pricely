import pytest
import json
from src.application.use_cases.delete_product import DeleteProductUseCase, ProductDeletingError
from src.application.use_cases.create_product import CreateProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.database.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
from src.domain.exceptions import ProductNotExistingDataBase, ProductDeletingError

def test_delete_product_use_case_success(
        mock_product_repo,
        mock_price_repo,
        mock_user_repo,
        product,
        price,
        user,
        mocker,
):
    '''Успешное удаление товара с ценой и пользователем.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=product)
    mocker.patch.object(mock_price_repo, 'get', return_value=price)
    mocker.patch.object(mock_user_repo, 'get', return_value=user)
    mocker.patch.object(mock_product_repo, 'delete', return_value=None)
    mocker.patch.object(mock_price_repo, 'delete', return_value=None)
    mocker.patch.object(mock_user_repo, 'save', return_value=None)

    # Создаем use case
    use_case = DeleteProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Выполняем удаление
    use_case.execute(product.id)

    # Проверяем вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    print(f"mock_price_repo.delete calls: {mock_price_repo.delete.mock_calls}")
    print(f"mock_product_repo.delete calls: {mock_product_repo.delete.mock_calls}")
    print(f"mock_user_repo.get calls: {mock_user_repo.get.mock_calls}")
    print(f"mock_user_repo.save calls: {mock_user_repo.save.mock_calls}")
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.delete.assert_called_once_with(product.price_id)
    mock_product_repo.delete.assert_called_once_with(product.id)
    mock_user_repo.get.assert_called_once_with(product.user_id)
    mock_user_repo.save.assert_called_once_with(user)
    assert product.id not in user.products  # Проверяем, что product.id удален из user.products

def test_delete_product_use_case_unsuccess(
        mock_product_repo,
        mock_price_repo,
        mock_user_repo,
        product,
        price,
        user,
        mocker,
):
    '''Проверяет, что выбрасывается исключение, если товар не существует.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=None)
    mocker.patch.object(mock_price_repo, 'get', return_value=None)
    mocker.patch.object(mock_user_repo, 'get', return_value=None)
    mocker.patch.object(mock_product_repo, 'delete', return_value=None)
    mocker.patch.object(mock_price_repo, 'delete', return_value=None)
    mocker.patch.object(mock_user_repo, 'save', return_value=None)

    # Создаем use case
    use_case = DeleteProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Проверяем, что выбрасывается ProductNotExistingDataBase
    with pytest.raises(ProductNotExistingDataBase, match=f'Товар {product.id} не существует в БД!'):
        use_case.execute(product.id)

    # Проверяем, что методы удаления и сохранения не вызывались
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.delete.assert_not_called()
    mock_product_repo.delete.assert_not_called()
    mock_user_repo.get.assert_not_called()
    mock_user_repo.save.assert_not_called()