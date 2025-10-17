import pytest
from src.infrastructure.database.mappers import ProductMapper
from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct

@pytest.mark.unit
def test_domain_to_orm(product):
    orm = ProductMapper.domain_to_orm(product)
    assert isinstance(orm, ORMProduct)
    assert orm.id == product.id
    assert orm.name == product.name

@pytest.mark.unit
def test_orm_to_domain(orm_product):
    domain = ProductMapper.orm_to_domain(orm_product)
    assert isinstance(domain, Product)
    assert domain.id == orm_product.id
    assert domain.link == orm_product.link