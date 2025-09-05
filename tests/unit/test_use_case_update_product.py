import pytest
import json
from datetime import datetime
from src.application.use_cases.upd_product import UpdateProductPriceUseCase
from src.domain.entities import Product, Price, User
from src.infrastructure.database.mappers import ProductMapper
from src.infrastructure.database.models import ORMUser
from src.domain.exceptions import ProductNotFoundError, PriceUpdateError


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
    # Проверяем, что продукт был получен
    pure_mock_product_repo.get.assert_called_once_with(product.id)

    # Проверяем, что цена сохранилась
    pure_mock_price_repo.save.assert_called_once_with(price_second)

    # Проверяем, что обновлённый продукт сохранился
    pure_mock_product_repo.save.assert_called_once_with(product)

    # И что продукт теперь указывает на новую цену
    assert product.price_id == price_second.id
    

    