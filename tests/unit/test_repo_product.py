import pytest
from sqlalchemy.exc import SQLAlchemyError

#from src.infrastructure.repositories import ProductRepositoryImpl
from src.infrastructure.database.models import ORMProduct
from src.domain.entities import Product
from src.infrastructure.mappers import ProductMapper

import logging
logger = logging.getLogger(__name__)

# ----- # ----- # ----- Фикстуры ORM слоя ----- # ----- # ----- #

def test_save_product_success(product_repo, product: Product, session):
    product_repo.save(product)
    saved_product = session.get(ORMProduct, product.id) # Прямой доступ к БД
    # Здесь можно использовать saved_product как в тесте ниже!!!!
    assert saved_product is not None
    assert saved_product.id == product.id

def test_get_product(product_repo, product, session):
    '''НУ И ПОЧЕМУ ОНИ ПОХОЖИ С ВЕРХНИМ??? '''
    product_repo.save(product)
    saved_product = product_repo.get(product_id=product.id)
    # saved_product лучше чем тот что ниже, так как мы используем методы репозитория
    #saved_product = session.get(ORMProduct, product.id)
    assert saved_product is not None
    assert saved_product.id == product.id
    assert saved_product.name == product.name

def test_get_product_not_found(product_repo, session):
    product_id = '6666666'
    product = product_repo.get(product_id=product_id)
    assert product == None

def test_delete_product(product_repo, product, session):
    product_repo.save(product)
    saved_product = product_repo.get(product_id=product.id)
    domain_saved_product = ProductMapper.orm_to_domain(saved_product)
    logger.debug(f'DOMAIN SAVED PRODUCT {domain_saved_product}')
    product_repo.delete(domain_saved_product.id)
    check_deleted_product = product_repo.get(product.id)
    assert check_deleted_product == None

def test_delete_product_not_found(product_repo):
    deleted = product_repo.delete('ID_ID')
    assert deleted is False

def test_get_all_products(product_repo, product, user):
    product_repo.save(product)
    saved_product_ORM = product_repo.get(product_id=product.id)
    result = product_repo.get_all(user.id)
    assert len(result) == 1