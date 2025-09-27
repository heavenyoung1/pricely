import pytest
from src.infrastructure.database.mappers import PriceMapper
from src.application.dto import PriceDTO
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice

@pytest.mark.unit
def test_dto_to_domain(price_dto):
    domain = PriceMapper.dto_to_domain(price_dto)
    assert isinstance(domain, Price)
    assert domain.id == None
    #assert domain.default == price_dto.default

@pytest.mark.unit
def test_domain_to_dto(price):
    dto = PriceMapper.domain_to_dto(price)
    assert isinstance(dto, PriceDTO)
    assert dto.id == price.id
    assert dto.created_at == price.created_at

@pytest.mark.unit
def test_domain_to_orm(price):
    orm = PriceMapper.domain_to_orm(price)
    assert isinstance(orm, ORMPrice)
    # id ещё не назначен, так как БД его сгенерирует
    assert orm.id is None
    #assert orm.default_price == price.default

@pytest.mark.unit
def test_orm_to_domain(orm_price):
    domain = PriceMapper.orm_to_domain(orm_price)
    assert isinstance(domain, Price)
    assert domain.id == orm_price.id
    assert domain.previous_with_card == orm_price.previous_with_card
    #assert domain.default == orm_price.default_price  # ✅ исправлено