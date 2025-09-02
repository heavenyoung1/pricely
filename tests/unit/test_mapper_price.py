import pytest
from src.infrastructure.database.mappers import PriceMapper
from src.application.dto import PriceDTO
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice


def test_dto_to_domain(price_dto):
    domain = PriceMapper.dto_to_domain(price_dto)
    assert isinstance(domain, Price)
    assert domain.id == price_dto.id
    assert domain.default == price_dto.default

def test_domain_to_dto(price):
    dto = PriceMapper.domain_to_dto(price)
    assert isinstance(dto, PriceDTO)
    assert dto.id == price.id
    assert dto.claim == price.claim

def test_domain_to_orm(price):
    orm = PriceMapper.domain_to_orm(price)
    assert isinstance(orm, ORMPrice)
    assert orm.id == price.id
    assert orm.default == price.default

def test_orm_to_domain(orm_price):
    domain = PriceMapper.orm_to_domain(orm_price)
    assert isinstance(domain, Price)
    assert domain.id == orm_price.id
    assert domain.previous_with_card == orm_price.previous_with_card