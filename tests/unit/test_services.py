import pytest
import logging
from unittest.mock import MagicMock
from src.infrastructure.repositories import PriceRepositoryImpl
from src.infrastructure.database.models import ORMPrice
from src.domain.entities import Price
from src.infrastructure.mappers import PriceMapper

logger = logging.getLogger(__name__)

def test_save_price_success(price, price_repo, session):
    '''Проверяет, что цена сохраняется в БД.'''
    price_repo.save(price)
    # Не вызываем session.commit(), так как UnitOfWork управляет транзакциями
    orm_price = session.get(ORMPrice, price.id)
    assert orm_price is not None
    assert orm_price.id == price.id
    assert orm_price.product_id == price.product_id
    assert orm_price.with_card == price.with_card
    assert orm_price.without_card == price.without_card
    assert orm_price.previous_with_card == price.previous_with_card
    assert orm_price.previous_without_card == price.previous_without_card
    assert orm_price.default == price.default
    assert orm_price.claim == price.claim

def test_get_price_success(price_repo, price, session):
    '''Проверяет, что метод get корректно возвращает цену.'''
    price_repo.save(price)
    result = price_repo.get(price.id)
    assert result.id == price.id
    assert result.product_id == price.product_id
    assert result.with_card == price.with_card
    assert result.without_card == price.without_card
    assert result.previous_with_card == price.previous_with_card
    assert result.previous_without_card == price.previous_without_card
    assert result.default == price.default
    assert result.claim == price.claim

def test_get_price_not_found(price_repo, session):
    '''Проверяет, что метод get возвращает None для несуществующей цены.'''
    result = price_repo.get("non_existent_id")
    assert result is None

def test_get_prices_by_product_success(price_repo, price, session):
    '''Проверяет получение списка цен продукта.'''
    price_repo.save(price)
    prices = price_repo.get_all_prices_by_product(price.product_id)
    assert len(prices) == 1
    assert prices[0].id == price.id
    assert prices[0].claim == price.claim

def test_get_prices_by_product_empty(price_repo, session):
    '''Проверяет, что возвращается пустой список для несуществующего продукта.'''
    prices = price_repo.get_all_prices_by_product("non_existent_id")
    assert prices == []

def test_delete_price_success(price_repo, price, session):
    '''Проверяет удаление цены.'''
    price_repo.save(price)
    deleted = price_repo.delete(price_id=price.id)
    assert deleted is True
    result = price_repo.get(price.id)
    assert result is None

def test_delete_price_not_found(price_repo, session):
    '''Проверяет удаление несуществующей цены.'''
    deleted = price_repo.delete(price_id="non_existent_id")
    assert deleted is False