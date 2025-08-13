import pytest
from sqlalchemy.exc import SQLAlchemyError

#from src.infrastructure.repositories import ProductRepositoryImpl
from src.infrastructure.database.models import ORMProduct
from src.domain.entities import Product
from src.infrastructure.mappers import ProductMapper

# ----- # ----- # ----- Фикстуры ORM слоя ----- # ----- # ----- #

def test_save_product(product_repo, product: Product, session):
    product_repo.save(product)
    saved_product = session.query(ORMProduct).get(product.id)
    print(saved_product)
    