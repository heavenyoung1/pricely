import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session

from src.domain.entities import Product, PriceStamp
from src.infrastructure.repositories.pg_product_repository import PGSQLProductRepository
from tests.fixtures.product import product_test

def test_product_to_orm_conversion(product_test):
    '''Проверяет, что метод to_orm() корректно конвертирует Product в DBProduct'''
    product = Product(**product_test)
    db_product = product.to_orm()

    assert db_product.product_id == product_test['product_id']
    assert db_product.user_id == product_test['user_id']
    assert db_product.name == product_test['name']
    assert db_product.rating == pytest.approx(product_test['rating'])  # Для float используем approx
    assert db_product.price_with_card == product_test['price_with_card']
    assert db_product.price_without_card == product_test['price_without_card']
    assert db_product.previous_price_with_card == product_test['previous_price_with_card']
    assert db_product.previous_price_without_card == product_test['previous_price_without_card']
    assert db_product.price_default == product_test['price_default']
    assert db_product.link == product_test['link']
    assert db_product.url_image == product_test['url_image']
    assert db_product.category_product == product_test['category_product']
    assert db_product.last_timestamp == product_test['last_timestamp']