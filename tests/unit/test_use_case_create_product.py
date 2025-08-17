import pytest
import json
from src.application.use_cases.create_product import CreateProductUseCase, ProductCreationError
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

# Юнит-тесты с моками
def test_product_create_success_mock(mock_product_repo, mock_price_repo, mock_user_repo, product, price, user):
    '''Тест успешного создания продукта с моками (юнит-тест).'''
    # Настраиваем моки: продукта нет, пользователь существует
    mock_product_repo.get.return_value = None
    mock_user_repo.get.return_value = user

    # Выполняем use case
    use_case = CreateProductUseCase(mock_product_repo, mock_price_repo, mock_user_repo)
    use_case.execute(product, price, user)

    mock_product_repo.get.assert_called_once_with(product.id)
    mock_user_repo.get.assert_called_once_with(user.id)
    mock_price_repo.save.assert_called_once_with(price)
    mock_product_repo.save.assert_called_once_with(product)
    mock_user_repo.save.assert_called_once_with(user)

    # Проверяем, что product.id добавлен в user.products
    assert product.id in user.products, 'Продукт не добавлен в список пользователя'

def test_product_create_already_exists_mock(mock_product_repo, mock_price_repo, mock_user_repo, product, price, user):
    """Тест ошибки, если продукт уже существует (юнит-тест с моками)."""
    # Настраиваем моки: продукт уже существует, пользователь существует
    mock_product_repo.get.return_value = product
    mock_user_repo.get.return_value = user

    use_case = CreateProductUseCase(mock_product_repo, mock_price_repo, mock_user_repo)

    