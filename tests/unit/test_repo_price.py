import pytest
import logging
from unittest.mock import MagicMock
from src.infrastructure.repositories import PriceRepositoryImpl
from src.infrastructure.database.models import ORMPrice
from src.domain.entities import Price

logger = logging.getLogger(__name__)

def test_save_price_succeess(price, price_repo, session):
    '''Проверяет, что цена сохраняется в БД.'''
    price_repo.save(price)
    session.commit()

    orm_price = session.get(ORMPrice, price.id)
    assert orm_price is not None
    assert orm_price.id == price.id
    assert orm_price.product_id == price.product_id
