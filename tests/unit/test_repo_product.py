import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.database.models import ORMProduct
from src.domain.entities import Product
from src.infrastructure.database.repositories import ProductRepositoryImpl
from src.infrastructure.database.mappers import ProductMapper

import logging
logger = logging.getLogger(__name__)

# ----- # ----- # ----- Тесты ----- # ----- # ----- #

def test_save_product_success(product_repo, product: Product, db_session):
    '''Проверяет, что продукт действительно сохранился в БД.'''
    product_repo.save(product)
    saved_product = db_session.get(ORMProduct, product.id) # Прямой доступ к БД
    assert saved_product is not None
    assert saved_product.id == product.id
    assert saved_product.name == product.name

@pytest.mark.unit
def test_save_product_success(product, mock_session, orm_product):
    repo = ProductRepositoryImpl(session=mock_session)

    # 1. Проверяем, что при первом вызове get() вернется None
    mock_session.get.return_value = None
    received_empty = repo.get(product_id=product.id)
    assert received_empty is None

    # 2. Выполняем save()
    repo.save(product)

    # 3. Теперь подсовываем ORM-модель, которую вернёт get()
    mock_session.get.return_value = orm_product
    received = repo.get(product_id=product.id)

    # Asserts
    assert received is not None
    assert received.id == product.id
    assert received.name == product.name

    mock_session.merge.assert_called_once()
    mock_session.get.assert_called_with(ORMProduct, product.id)

@pytest.mark.unit
def test_save_price_unsuccess(product, mock_session):
    repo = ProductRepositoryImpl(session=mock_session)
    received_empty = repo.get(product_id=product.id)
    assert received_empty is None
    #repo.save('NON_PRODUCTS')


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

def test_delete_product(product_repo, product, db_session):
    '''Проверка, что delete реально удаляет объект из БД.'''
    product_repo.save(product)
    assert db_session.get(ORMProduct, product.id) is not None  # Есть до удаления

    deleted = product_repo.delete(product.id)
    db_session.commit()  # Фиксируем изменения в базе
    assert deleted is True
    assert db_session.get(ORMProduct, product.id) is None

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


    #АХАХАХ, тут воолбщзе не тот репо
    # ИСПОЛЬЗУЙ PRODUCT REPO!!! 
# @pytest.mark.unit
# def test_get_relevant_price_id_found(mock_session, price, orm_product):
#     repo = PriceRepositoryImpl(session=mock_session)
#     mock_session.get.return_value = orm_product

#     result = repo.get_relevant_price_id(product_id=price.product_id)
#     logger.info(f'RESULT: {result}')
#     assert result == price.id