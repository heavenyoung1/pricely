from abc import ABC, abstractmethod
from domain.entities.product import Product
from typing import List

class ProductRepository(ABC):
    @abstractmethod
    def get_product_data(self, url: str) -> Product:
        pass