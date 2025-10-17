import pytest
from src.infrastructure.database.mappers import PriceMapper
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice

@pytest.mark.unit
def test_domain_to_orm(price):
    orm = PriceMapper.domain_to_orm(price)
    assert isinstance(orm, ORMPrice)
    # id ещё не назначен, так как БД его сгенерирует
    assert orm.id is None

@pytest.mark.unit
def test_orm_to_domain(orm_price):
    domain = PriceMapper.orm_to_domain(orm_price)
    assert isinstance(domain, Price)
    assert domain.id == orm_price.id
    assert domain.previous_with_card == orm_price.previous_with_card