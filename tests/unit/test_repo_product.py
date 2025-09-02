import pytest
from sqlalchemy.exc import SQLAlchemyError

#from src.infrastructure.repositories import ProductRepositoryImpl
from src.infrastructure.database.models import ORMProduct
from src.domain.entities import Product
from src.infrastructure.database.repositories import PriceRepositoryImpl
from src.infrastructure.database.mappers import ProductMapper

import logging
logger = logging.getLogger(__name__)

# ----- # ----- # ----- Тесты ----- # ----- # ----- #

def test_save_product_success(product_repo, product: Product, session):
    '''Проверяет, что продукт действительно сохранился в БД.'''
    product_repo.save(product)
    saved_product = session.get(ORMProduct, product.id) # Прямой доступ к БД
    assert saved_product is not None
    assert saved_product.id == product.id
    assert saved_product.name == product.name

def test_get_product(product_repo, product):
    '''Проверяет, что метод репозитория get корректно возвращает продукт.'''
    product_repo.save(product)
    retrieved  = product_repo.get(product_id=product.id) # Через API репозитория
    assert retrieved is not None
    assert retrieved.id == product.id
    assert retrieved.name == product.name

def test_get_product_not_found(product_repo):
    '''Проверка, что get возвращает None для несуществующего продукта.'''
    product_id = '666'
    product = product_repo.get(product_id=product_id)
    assert product is None

def test_delete_product(product_repo, product, session):
    '''Проверка, что delete реально удаляет объект из БД.'''
    product_repo.save(product)
    assert session.get(ORMProduct, product.id) is not None  # Есть до удаления

    deleted = product_repo.delete(product.id)
    session.commit()  # Фиксируем изменения в базе
    assert deleted is True
    assert session.get(ORMProduct, product.id) is None

def test_delete_product_not_found(product_repo):
    '''Удаление несуществующего объекта должно вернуть False.'''
    deleted = product_repo.delete('ID_ID')
    assert deleted is False

def test_get_all_products(product_repo, product, user):
    '''Проверка, что get_all возвращает все товары пользователя.'''
    product_repo.save(product)
    result = product_repo.get_all(user.id)
    assert len(result) == 1
    assert result[0].id == product.id