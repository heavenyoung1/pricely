import pytest
import json
from src.application.use_cases.upd_price import UpdatePriceUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_upd_price_use_case_success(
        mock_product_repo, 
        mock_price_repo, 
        product, 
        price, 
    ):
    '''Успешное обновление цены товара.'''
    mock_product_repo.get.return_value = product
    mock_price_repo.get.return_value = price

    # Создаём use case
    use_case = UpdatePriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo
    )
    use_case.execute(price=price, product_id=product.id)

    mock_price_repo.save.assert_called_once_with(price)
    mock_product_repo.get.assert_called_once_with(product.id)
    assert product.price_id == price.id
    mock_product_repo.save.assert_called_once_with(product)

def test_update_price_product_not_found(mock_product_repo, mock_price_repo, price):
    '''Ошибка, если продукт не найден.'''
    mock_product_repo.get.return_value = None

    # Создаём use case
    use_case = UpdatePriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo
    )

    with pytest.raises(ValueError, match=f'Продукт с id ID_IS не найден'):
        use_case.execute(price=price, product_id='ID_IS')

