import pytest
from src.infrastructure.database.mappers import ProductMapper
from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct


@pytest.mark.unit
def test_domain_to_orm(product: Product):
    orm_product = ProductMapper.domain_to_orm(product)
    assert isinstance(orm_product, ORMProduct)
    # Проверка, что поля соответствуют между доменной моделью и ORM моделью
    assert_products_equal(orm_product, product)


@pytest.mark.unit
def test_orm_to_domain(orm_product: ORMProduct):
    domain_product = ProductMapper.orm_to_domain(orm_product)
    assert isinstance(domain_product, Product)
    assert_products_equal(orm_product, domain_product)


def assert_products_equal(orm_product, domain_product):
    """
    Универсальная функция для сравнения объектов Product и ORMProduct.
    Проверяет, что все поля соответствуют друг другу.

    Аргументы:
        orm_product (ORMProduct): Объект ORM (ORMProduct), который нужно проверить.
        domain_product (Product): Объект доменной модели (Product), с которым будем сравнивать.
    """
    assert (
        orm_product.id == domain_product.id
    ), f"Несоответствие ID: {orm_product.id} != {domain_product.id}"
    assert (
        orm_product.name == domain_product.name
    ), f"Несоответствие имени: {orm_product.name} != {domain_product.name}"
    assert (
        orm_product.link == domain_product.link
    ), f"Несоответствие ссылки: {orm_product.link} != {domain_product.link}"
    assert (
        orm_product.image_url == domain_product.image_url
    ), f"Несоответствие URL изображения: {orm_product.image_url} != {domain_product.image_url}"
    assert (
        orm_product.rating == domain_product.rating
    ), f"Несоответствие рейтинга: {orm_product.rating} != {domain_product.rating}"
    assert (
        orm_product.categories == domain_product.categories
    ), f"Несоответствие категорий: {orm_product.categories} != {domain_product.categories}"
