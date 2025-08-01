import pytest
from datetime import datetime
from src.domain.entities.product import Product
from typing import List, TYPE_CHECKING
from tests.fixtures.product import product_test


from src.infrastruture.database.models.product import DBProduct


def test_product_to_orm_conversion(product_test):
    '''Проверяет, что метод to_orm() корректно конвертирует Product в DBProduct'''
    product = Product(**product_test)

    db_product = product.to_orm()

    # Assert
    assert isinstance(db_product, DBProduct)  # Проверяем тип
    assert db_product.product_id == product_test['product_id']
