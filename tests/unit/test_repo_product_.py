import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.infrastructure.repositories import ProductRepositoryImpl
from src.infrastructure.database.models import ORMProduct
from src.domain.entities import Product
from src.infrastructure.mappers import ProductMapper

# ----- # ----- # ----- Фикстуры ORM слоя ----- # ----- # ----- #

def test_save_new_product(session, repository, product):
    repos