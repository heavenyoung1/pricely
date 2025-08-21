import pytest
import json
from src.application.use_cases.create_product import CreateProductUseCase, ProductCreationError
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_create_product_use_case_success(
        mock_product_repo, 
        mock_price_repo, 
        mock_user_repo, 
        product, 
        price, 
        user,
    ):
    
    # Настраиваем моки
    mock_user_repo.get.return_value = user      # Пользователь существует
    mock_product_repo.get.return_value = None   # Товар не существует

    # Создаём use case
    use_case = CreateProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )
    # Выполняем создание продукта
    use_case.execute(product=product, price=price, user_id=user.id)

    # Проверяем, что price_id обновлён
    assert product.price_id == price.id, 'price_id товара не обновлен'

    # Проверяем, что продукт добавлен в список пользователя
    assert product.id in user.products, f'Товар {product.id} не добавлен пользователю'

    mock_user_repo.get.assert_called_once_with(user.id)
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.save.assert_called_once_with(price)
    mock_user_repo.save.assert_called_once_with(user)
    mock_product_repo.save.assert_called_once_with(product)

def test_create_product_use_case_product_exists(
        mock_product_repo, 
        mock_price_repo, 
        mock_user_repo, 
        product, 
        price, 
        user,
):
    '''Юнит-тест: ошибка, если продукт уже существует.'''
    # Настраиваем моки
    mock_user_repo.get.return_value = user      # Пользователь существует
    mock_product_repo.get.return_value = product   # Товар не существует

    # Создаём use case
    use_case = CreateProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Выполняем создание товара
    with pytest.raises(ProductCreationError, match=f'Товар {product.id} уже существует'):
        use_case.execute(product=product, user_id=user.id, price=price)

    mock_user_repo.get.assert_called_once_with(user.id)
    mock_product_repo.get.assert_called_once_with(product.id)
    assert not mock_price_repo.save.called, 'save (цена) не должен быть вызван'
    assert not mock_product_repo.save.called, 'save (продукт) не должен быть вызван'
    assert not mock_user_repo.save.called, 'save (пользователь) не должен быть вызван'


def test_create_product_use_case_user_not_found(mock_product_repo, mock_price_repo, mock_user_repo, product, price, user):
    '''Юнит-тест: ошибка, если пользователь не найден.'''
    mock_user_repo.get.return_value = None      # Пользователь НЕ существует

    # Создаём use case
    use_case = CreateProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Выполняем создание товара
    with pytest.raises(ProductCreationError, match=f'Пользователь {user.id} не найден'):
        use_case.execute(product=product, user_id=user.id, price=price)