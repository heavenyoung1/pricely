from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.product import Product
from src.interfaces.repositories.product_repository import ProductRepository
from domain.entities.price_claim import PriceStamp


# class JSONProductRepository(ProductRepository):
#     def save:
#         pass