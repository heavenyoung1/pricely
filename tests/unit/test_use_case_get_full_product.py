import pytest
import json
from src.application.use_cases.get_full_product import GetFullProductUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.database.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
from src.domain.exceptions import ProductNotFoundError

def test_get_full_product_use_case_success(
        mock_product_repo,
        mock_price_repo,
        mock_user_repo,
        product,
        price,
        user,
        mocker,
):
    '''Успешное получение полной информации о товаре.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=product)
    mocker.patch.object(mock_price_repo, 'get', return_value=price)
    mocker.patch.object(mock_user_repo, 'get', return_value=user)

    # Создаем use case
    use_case = GetFullProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Выполняем
    result = use_case.execute(product_id=product.id)

    # Проверяем результат и вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    print(f"mock_price_repo.get calls: {mock_price_repo.get.mock_calls}")
    print(f"mock_user_repo.get calls: {mock_user_repo.get.mock_calls}")
    assert result == {'product': product, 'price': price, 'user': user}
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.get.assert_called_once_with(product.price_id)
    mock_user_repo.get.assert_called_once_with(product.user_id)

def test_get_full_product_not_found(
        mock_product_repo,
        mock_price_repo,
        mock_user_repo,
        mocker,
):
    '''Проверяет, что выбрасывается ProductNotFoundError, если продукт не существует.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=None)
    mocker.patch.object(mock_price_repo, 'get', return_value=None)
    mocker.patch.object(mock_user_repo, 'get', return_value=None)

    # Создаем use case
    use_case = GetFullProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Проверяем, что выбрасывается ProductNotFoundError
    with pytest.raises(ProductNotFoundError, match='Товар ID_ID не существует'):
        use_case.execute(product_id='ID_ID')

    # Проверяем вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    mock_product_repo.get.assert_called_once_with('ID_ID')
    mock_price_repo.get.assert_not_called()
    mock_user_repo.get.assert_not_called()

def test_get_full_product_no_price(
        mock_product_repo,
        mock_price_repo,
        mock_user_repo,
        product,
        user,
        mocker,
):
    '''Проверяет получение продукта без цены (price_id=None).'''
    # Создаем продукт без price_id
    product_no_price = Product(
        id=product.id,
        user_id=product.user_id,
        price_id=None,
        name=product.name,
        link=product.link,
        image_url=product.image_url,
        rating=product.rating,
        categories=product.categories
    )

    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=product_no_price)
    mocker.patch.object(mock_price_repo, 'get', return_value=None)
    mocker.patch.object(mock_user_repo, 'get', return_value=user)

    # Создаем use case
    use_case = GetFullProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Выполняем
    result = use_case.execute(product_id=product.id)

    # Проверяем результат и вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    print(f"mock_price_repo.get calls: {mock_price_repo.get.mock_calls}")
    print(f"mock_user_repo.get calls: {mock_user_repo.get.mock_calls}")
    assert result == {'product': product_no_price, 'price': None, 'user': user}
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.get.assert_not_called()
    mock_user_repo.get.assert_called_once_with(product.user_id)

def test_get_full_product_no_user(
        mock_product_repo,
        mock_price_repo,
        mock_user_repo,
        product,
        price,
        mocker,
):
    '''Проверяет получение продукта без пользователя.'''
    # Настраиваем моки
    mocker.patch.object(mock_product_repo, 'get', return_value=product)
    mocker.patch.object(mock_price_repo, 'get', return_value=price)
    mocker.patch.object(mock_user_repo, 'get', return_value=None)

    # Создаем use case
    use_case = GetFullProductUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
        user_repo=mock_user_repo,
    )

    # Выполняем
    result = use_case.execute(product_id=product.id)

    # Проверяем результат и вызовы
    print(f"mock_product_repo.get calls: {mock_product_repo.get.mock_calls}")
    print(f"mock_price_repo.get calls: {mock_price_repo.get.mock_calls}")
    print(f"mock_user_repo.get calls: {mock_user_repo.get.mock_calls}")
    assert result == {'product': product, 'price': price, 'user': None}
    mock_product_repo.get.assert_called_once_with(product.id)
    mock_price_repo.get.assert_called_once_with(product.price_id)
    mock_user_repo.get.assert_called_once_with(product.user_id)