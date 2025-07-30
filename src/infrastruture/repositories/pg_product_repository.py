from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.product import Product
from src.interfaces.repositories.product_repository import ProductRepository
from src.domain.entities.price import PriceStamp

from infrastruture.database.core.database import engine, SessionFactory
from src.infrastruture.database.models.base import Base


class PGSQLProductRepository(ProductRepository):
    def __init__(self):
        self.engine = engine
        self.session = SessionFactory
        Base.metadata.create_all(self.engine)

        