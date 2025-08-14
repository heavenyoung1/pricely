import pytest
import logging
from unittest.mock import MagicMock
from src.infrastructure.repositories import PriceRepositoryImpl
from src.infrastructure.database.models import ORMPrice
from src.domain.entities import Price
from src.infrastructure.mappers import PriceMapper

logger = logging.getLogger(__name__)

def test_save_price_succeess(price, price_repo, session):
    '''Проверяет, что цена сохраняется в БД.'''
    price_repo.save(price)
    session.commit()

    orm_price = session.get(ORMPrice, price.id)
    assert orm_price is not None
    assert orm_price.id == price.id
    assert orm_price.product_id == price.product_id


def test_get_price(price_repo, price, session):
    '''Проверяет, что метод репозитория get корректно возвращает цену.'''
    price_repo.save(price)
    session.commit()

    orm_price_by_BD = session.get(ORMPrice, price.id)
    price_by_bd = PriceMapper.orm_to_domain(orm_price_by_BD)
    price_by_API = price_repo.get(price.id)
    assert price_by_bd.id == price.id
    assert price_by_API.id == price.id

def test_get_prices_by_product(price_repo, price, session):
    '''Проверяет получение списка цен продукта.'''
    price_repo.save(price)
    session.commit()

    prices_product_by_API = price_repo.get_prices_by_product(price.product_id)
    assert len(prices_product_by_API) == 1
    assert prices_product_by_API[0].id == price.id
    assert prices_product_by_API[0].claim == price.claim
    
