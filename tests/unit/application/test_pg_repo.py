# import pytest
# from unittest.mock import Mock, create_autospec
# from sqlalchemy.orm import Session

# from src.domain.entities import Product, PriceStamp
# from src.infrastructure.repositories.pg_product_repository import PGSQLProductRepository
# from tests.fixtures.product import product_test
#--------------------------------------------------

# Пока что не нужен
# def test_product_to_orm_conversion(product_test):
#     '''Проверяет, что метод to_orm() корректно конвертирует Product в DBProduct'''
#     product = Product(**product_test)
#     db_product = product.to_orm()

#     assert db_product.product_id == product_test['product_id']
#     assert db_product.user_id == product_test['user_id']
#     assert db_product.name == product_test['name']
#     assert db_product.rating == pytest.approx(product_test['rating'])  # Для float используем approx
#     assert db_product.price_with_card == product_test['price_with_card']
#     assert db_product.price_without_card == product_test['price_without_card']
#     assert db_product.previous_price_with_card == product_test['previous_price_with_card']
#     assert db_product.previous_price_without_card == product_test['previous_price_without_card']
#     assert db_product.price_default == product_test['price_default']
#     assert db_product.link == product_test['link']
#     assert db_product.url_image == product_test['url_image']
#     assert db_product.category_product == product_test['category_product']
#     assert db_product.last_timestamp == product_test['last_timestamp']

from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.product import DBProduct
from src.infrastructure.database.models.price_stamp import DBPriceStamp
from src.infrastructure.repositories.pg_product_repository import PGSQLProductRepository


def test_save_one_product_unit(repo, product, price_stamp):
    with patch.object(Product, 'to_orm', return_value=MagicMock(spec=DBProduct)) as mock_to_orm, \
        patch.object(PriceStamp, 'to_orm', return_value=MagicMock(spec=DBPriceStamp)) as mock_price_to_orm, \
        patch.object(repo.session, 'merge') as mock_merge, \
        patch.object(repo.session, 'add') as mock_add, \
        patch.object(repo.session, 'commit') as mock_commit:

        repo.save_one_product(product, price_stamp)

        mock_to_orm.assert_called_once()
        mock_price_to_orm.assert_called_once()
        mock_merge.assert_called_once()
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

def test_save_few_products_unit(repo, product, price_stamp):
    products = [product, product]  # Два одинаковых продукта для теста
    price_stamps = [price_stamp, price_stamp]  # Передаём price_stamp как список
    with patch.object(Product, 'to_orm', return_value=MagicMock(spec=DBProduct)) as mock_to_orm, \
         patch.object(PriceStamp, 'to_orm', return_value=MagicMock(spec=DBPriceStamp)) as mock_price_to_orm, \
         patch.object(repo.session, 'bulk_save_objects') as mock_bulk_save, \
         patch.object(repo.session, 'add') as mock_add, \
         patch.object(repo.session, 'commit') as mock_commit:

        repo.save_few_products(products, price_stamps)

        assert mock_to_orm.call_count == 2  # Вызывается для каждого продукта
        assert mock_price_to_orm.call_count == 2  # Вызывается для каждого price_stamp
        mock_bulk_save.assert_called_once()
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

def test_find_product_by_url_unit(repo, product):
    mock_db_product = MagicMock(spec=DBProduct)
    mock_db_product.to_domain.return_value = product
    with patch.object(repo.session, 'query', return_value=MagicMock()) as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = mock_db_product

        result = repo.find_product_by_url('https://example.com')

        mock_query.assert_called_once_with(DBProduct)
        mock_query.return_value.filter.assert_called_once()
        mock_db_product.to_domain.assert_called_once()
        assert result == product

def test_find_product_by_url_not_found_unit(repo):
    with patch.object(repo.session, 'query', return_value=MagicMock()) as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = None

        result = repo.find_product_by_url('https://example.com')

        mock_query.assert_called_once_with(DBProduct)
        mock_query.return_value.filter.assert_called_once()
        assert result is None