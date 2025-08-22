import pytest
import json
from src.application.use_cases.upd_product import UpdateProductPriceUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser

def test_get_full_product_use_case_success(
        mock_product_repo, 
        mock_price_repo,  
        product, 
        price, 
        user,
    ):
    '''Успешное обновление цены через продукт.'''

    # Настраиваем моки: продукт существует
    mock_product_repo.get.return_value = product

    # Создаём use case
    use_case = UpdateProductPriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
    )

    use_case.execute(product=product, price=price)
    mock_price_repo.save.assert_called_once_with(price)
    mock_product_repo.save.assert_called_once_with(product)
    assert product.price_id == price.id

def test_update_product_price_product_not_found(
        mock_product_repo, 
        mock_price_repo, 
        product, 
        price):
    '''Ошибка, если продукт не найден.'''

    mock_product_repo.get.return_value = None
    use_case = UpdateProductPriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo,
    )

    with pytest.raises(ValueError, match='Продукт не найден'):
        use_case.execute(product=product, price=price)

    mock_price_repo.save.assert_not_called()
    mock_product_repo.save.assert_not_called()