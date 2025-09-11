import pytest
from src.infrastructure.database.mappers import ProductMapper
from src.application.dto import ProductDTO
from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct

@pytest.mark.unit
def test_dto_to_domain(product_dto):
    domain = ProductMapper.dto_to_domain(product_dto)
    assert isinstance(domain, Product)
    assert domain.id == product_dto.id
    assert domain.name == product_dto.name

@pytest.mark.unit
def test_domain_to_dto(product):
    dto = ProductMapper.domain_to_dto(product)
    assert isinstance(dto, ProductDTO)
    assert str(dto.link) == product.link
    assert str(dto.image_url) == product.image_url
    assert dto.rating == product.rating
    assert dto.categories == product.categories

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