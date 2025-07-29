from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.product import Product
from src.interfaces.repositories.product_repository import ProductRepository
from src.domain.entities.price import PriceStamp


class PGSQLProductRepository(ProductRepository):
    pass