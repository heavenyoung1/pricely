from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.domain.entities.product import Product
from domain.entities.price_claim import PriceStamp
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.product import DBProduct
from src.infrastructure.database.models.price_stamp import DBPriceStamp
from src.infrastructure.repositories.pg_product_repository import PGSQLProductRepository

'''
Тестирование методов репозитория PGSQLProductRepository.
Все тесты являются юнит-тестами и используют патчи для изоляции внешних зависимостей.
'''

def test_save_one_product_unit(repo, product, price_stamp):
    '''
    Тестирует метод save_one_product:
    Проверяет, что объекты Product и PriceStamp корректно конвертируются в ORM-модели
    и сохраняются в базу данных через методы merge, add и commit.
    '''
    with patch.object(Product, 'to_orm', return_value=MagicMock(spec=DBProduct)) as mock_to_orm, \
        patch.object(PriceStamp, 'to_orm', return_value=MagicMock(spec=DBPriceStamp)) as mock_price_to_orm, \
        patch.object(repo.session, 'merge') as mock_merge, \
        patch.object(repo.session, 'add') as mock_add, \
        patch.object(repo.session, 'commit') as mock_commit:

        repo.save_one_product(product, price_stamp)

        mock_to_orm.assert_called_once()              # Проверяем, что конвертация продукта была вызвана
        mock_price_to_orm.assert_called_once()        # Проверяем, что конвертация цены была вызвана
        mock_merge.assert_called_once()               # Проверяем, что merge был вызван
        mock_add.assert_called_once()                 # Проверяем, что add был вызван
        mock_commit.assert_called_once()              # Проверяем, что commit был вызван

def test_save_few_products_unit(repo, product, price_stamp):
    '''
    Тестирует метод save_few_products:
    Проверяет, что несколько объектов Product и PriceStamp корректно конвертируются и сохраняются в базу.
    '''
    products = [product, product]                    # Используем два одинаковых объекта продукта
    price_stamps = [price_stamp, price_stamp]        # Используем два одинаковых объекта цены

    with patch.object(Product, 'to_orm', return_value=MagicMock(spec=DBProduct)) as mock_to_orm, \
         patch.object(PriceStamp, 'to_orm', return_value=MagicMock(spec=DBPriceStamp)) as mock_price_to_orm, \
         patch.object(repo.session, 'bulk_save_objects') as mock_bulk_save, \
         patch.object(repo.session, 'add') as mock_add, \
         patch.object(repo.session, 'commit') as mock_commit:

        repo.save_few_products(products, price_stamps)

        assert mock_to_orm.call_count == 2            # Проверяем, что to_orm вызван дважды для продуктов
        assert mock_price_to_orm.call_count == 2      # Проверяем, что to_orm вызван дважды для цен
        mock_bulk_save.assert_called_once()           # bulk_save_objects должен быть вызван
        mock_add.assert_called_once()                 # add вызывается один раз
        mock_commit.assert_called_once()              # commit вызывается один раз

def test_find_product_by_url_unit(repo, product):
    '''
    Тестирует метод find_product_by_url:
    Проверяет, что если продукт найден в БД по URL, он корректно преобразуется обратно в доменную сущность.
    '''
    mock_db_product = MagicMock(spec=DBProduct)
    mock_db_product.to_domain.return_value = product
    with patch.object(repo.session, 'query', return_value=MagicMock()) as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = mock_db_product

        result = repo.find_product_by_url('https://example.com')

        mock_query.assert_called_once_with(DBProduct)
        mock_query.return_value.filter.assert_called_once()
        mock_db_product.to_domain.assert_called_once()
        assert result == product                     # Результат должен быть эквивалентен оригинальному продукту

def test_find_product_by_url_not_found_unit(repo):
    '''
    Тестирует метод find_product_by_url:
    Проверяет, что если продукт не найден по URL, метод возвращает None.
    '''
    with patch.object(repo.session, 'query', return_value=MagicMock()) as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = None

        result = repo.find_product_by_url('https://example.com')

        mock_query.assert_called_once_with(DBProduct)
        mock_query.return_value.filter.assert_called_once()
        assert result is None                        # Ожидаем None, если продукт не найден

def test_find_product_by_id_unit(repo, product):
    '''
    Тестирует метод find_product_by_id:
    Проверяет, что при наличии продукта с указанным ID он корректно возвращается как доменная сущность.
    '''
    mock_db_product = MagicMock(spec=DBProduct)
    mock_db_product.to_domain.return_value = product

    with patch.object(repo.session, 'query', return_value=MagicMock()) as mock_query:
        mock_query.return_value.filter.return_value.first.return_value = mock_db_product

        result = repo.find_product_by_id('prod1')

        mock_query.assert_called_once_with(DBProduct)
        mock_query.return_value.filter.assert_called_once()
        mock_db_product.to_domain.assert_called_once()
        assert result == product

def test_find_few_products_by_urls_unit(repo, product):
    '''
    Тестирует метод find_few_products_by_urls:
    Проверяет, что при запросе нескольких URL возвращается список соответствующих продуктов.
    '''
    mock_db_product = MagicMock(spec=DBProduct)
    mock_db_product.to_domain.return_value = product
    with patch.object(repo.session, 'query', return_value=MagicMock()) as mock_query:
        mock_query.return_value.filter.return_value.all.return_value = [mock_db_product, mock_db_product]

        result = repo.find_few_products_by_urls(['https://example.com/1', 'https://example.com/2'])

        mock_query.assert_called_once_with(DBProduct)
        mock_query.return_value.filter.assert_called_once()
        assert mock_db_product.to_domain.call_count == 2     # Два продукта должны быть конвертированы
        assert len(result) == 2
        assert result == [product, product]