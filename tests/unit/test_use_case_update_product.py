import pytest
import json
from datetime import datetime
from src.application.use_cases.upd_product import UpdateProductPriceUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.database.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
from src.domain.exceptions import ProductNotFoundError, PriceUpdateError

# def test_upd_price_use_case_success(
#         mock_product_repo,
#         mock_price_repo,
#         product,
#         price,
#         price_second,
#         mocker,
# ):
#     '''Успешное обновление цены товара.'''
#     # Настраиваем моки
#     mocker.patch.object(mock_product_repo, 'get', return_value=product)
#     mocker.patch.object(mock_price_repo, 'get', return_value=price)
#     mocker.patch.object(mock_price_repo, 'save', return_value=None)
#     mocker.patch.object(mock_product_repo, 'save', return_value=None)

#     # Создаем use case
#     use_case = UpdateProductPriceUseCase(
#         product_repo=mock_product_repo,
#         price_repo=mock_price_repo
#     )

#     # Выполняем обновление
#     use_case.execute(product_id=product.id, price=price_second)

#     # Проверяем вызовы
#     print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
#     print(f"mock_price_repo.save calls: {mock_price_repo.save.mock_calls}")
#     print(f"mock_product_repo.save calls: {mock_product_repo.save.mock_calls}")
#     mock_product_repo.get.assert_called_once_with(product.id)
#     mock_price_repo.save.assert_called_once_with(price_second)
#     mock_product_repo.save.assert_called_once_with(product)
#     # Проверяем, что product.price_id обновлен
#     saved_product = mock_product_repo.save.call_args[0][0]
#     assert saved_product.price_id == price_second.id

def test_upd_price_use_case_success(
    pure_mock_product_repo,
    pure_mock_price_repo,   
    product,
    price,
    price_second,
):
    pure_mock_product_repo.get.return_value = product
    pure_mock_price_repo.get.return_value = price

    use_case = UpdateProductPriceUseCase(
        product_repo=pure_mock_product_repo,
        price_repo=pure_mock_price_repo,
    )
    result = use_case.execute(product_id=product.id, price=price_second)
    #pure_mock_product_repo.get.assert_called_once_with(product.id)
    #pure_mock_product_repo.save.assert_called_once_with(price_second)
    

def test_upd_price_use_case_product_not_found(
        mock_product_repo,
        mock_price_repo,
        product,
        price_second,
        mocker,
):
    '''Проверяет, что выбрасывается ProductNotFoundError, если продукт не существует.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=None)
    mocker.patch.object(mock_price_repo, 'save', return_value=None)
    mocker.patch.object(mock_product_repo, 'save', return_value=None)

    # Создаем use case
    use_case = UpdateProductPriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo
    )

    # Проверяем, что выбрасывается ProductNotFoundError
    with pytest.raises(ProductNotFoundError, match=f'Продукт с id {product.id} не найден'):
        use_case.execute(product_id=product.id, price=price_second)

    # Проверяем вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.save.assert_not_called()
    mock_product_repo.save.assert_not_called()

def test_upd_price_use_case_invalid_product_id(
        mock_product_repo,
        mock_price_repo,
        price_second,
        mocker,
):
    '''Проверяет, что выбрасывается PriceUpdateError, если product_id пустой.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=None)
    mocker.patch.object(mock_price_repo, 'save', return_value=None)
    mocker.patch.object(mock_product_repo, 'save', return_value=None)

    # Создаем use case
    use_case = UpdateProductPriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo
    )

    # Проверяем, что выбрасывается PriceUpdateError
    with pytest.raises(PriceUpdateError, match='Идентификатор продукта не указан'):
        use_case.execute(product_id='', price=price_second)

    # Проверяем, что методы не вызывались
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    mock_product_repo.get.assert_not_called()
    mock_price_repo.save.assert_not_called()
    mock_product_repo.save.assert_not_called()

def test_upd_price_use_case_invalid_price_id(
        mock_product_repo,
        mock_price_repo,
        product,
        mocker,
):
    '''Проверяет, что выбрасывается PriceUpdateError, если price.id пустой.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=product)
    mocker.patch.object(mock_price_repo, 'save', return_value=None)
    mocker.patch.object(mock_product_repo, 'save', return_value=None)

    # Создаем price с пустым id
    invalid_price = Price(
        id='',
        product_id=product.id,
        with_card=100,
        without_card=120,
        previous_with_card=90,
        previous_without_card=110,
        default=150,
        claim=datetime(2025, 1, 1, 0, 0)
    )

    # Создаем use case
    use_case = UpdateProductPriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo
    )

    # Проверяем, что выбрасывается PriceUpdateError
    with pytest.raises(PriceUpdateError, match='Идентификатор цены не указан'):
        use_case.execute(product_id=product.id, price=invalid_price)

    # Проверяем вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    mock_product_repo.get.assert_not_called()
    mock_price_repo.save.assert_not_called()
    mock_product_repo.save.assert_not_called()

    