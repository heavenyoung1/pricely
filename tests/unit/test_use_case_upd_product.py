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
    ):
    '''Успешное обновление цены товара.'''
    mock_product_repo.get.return_value = product
    mock_price_repo.get.return_value = price

    # Создаём use case
    use_case = UpdateProductPriceUseCase(
        product_repo=mock_product_repo,
        price_repo=mock_price_repo
    )
    use_case.execute(product_id=product.id, price=price)

    mock_price_repo.save.assert_called_once_with(price)
    mock_product_repo.get.assert_called_once_with(product.id)
    assert product.price_id == price.id
    mock_product_repo.save.assert_called_once_with(product)


