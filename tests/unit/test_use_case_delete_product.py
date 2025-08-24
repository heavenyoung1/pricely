import pytest
import json
from src.application.use_cases.delete_product import DeleteProductUseCase, ProductDeletingError
from application.use_cases.create_product_old import CreateProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_delete_product_use_case_success(
        mock_product_repo, 
        mock_price_repo, 
        mock_user_repo, 
        product, 
        price, 
        user,
    ):
    '''Успешное удаление товара с ценой и пользователем.'''

    # Настраиваем моки: продукт существует, пользователь тоже
    mock_product_repo.get.return_value = product
    mock_user_repo.get.return_value = user

    use_case = DeleteProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Выполняем удаление
    use_case.execute(product.id)

    # Проверяем, что цена удалена
    mock_price_repo.delete.assert_called_once_with(product.price_id)

    # Проверяем, что товар удалён
    mock_product_repo.delete.assert_called_once_with(product.id)

    assert product.id not in user.products
    mock_user_repo.save.assert_called_once_with(user)


