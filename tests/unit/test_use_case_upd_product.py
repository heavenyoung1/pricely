import pytest
import json
from src.application.use_cases.upd_product import UpdateProductPriceUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
from src.application.exceptions import ProductNotFoundError, PriceUpdateError

def test_upd_price_use_case_success(
        mock_product_repo,
        mock_price_repo,
        product,
        price,
        price_second,
        mocker,
):
    '''Успешное обновление цены товара.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=product)
    mocker.patch.object(mock_price_repo, 'get', return_value=price)
    mocker.patch.object(mock_price_repo, 'save', return_value=None)
    mocker.patch.object(mock_product_repo, 'save', return_value=None)

    # Создаем use case
    use_case = UpdateProductPriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo
    )

    # Выполняем обновление
    use_case.execute(product_id=product.id, price=price_second)

    # Проверяем вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    print(f"mock_price_repo.save calls: {mock_price_repo.save.mock_calls}")
    print(f"mock_product_repo.save calls: {mock_product_repo.save.mock_calls}")
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.save.assert_called_once_with(price_second)
    mock_product_repo.save.assert_called_once_with(product)
    # Проверяем, что product.price_id обновлен
    saved_product = mock_product_repo.save.call_args[0][0]
    assert saved_product.price_id == price_second.id


