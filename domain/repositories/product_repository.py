from abc import ABC, abstractmethod
from domain.entities.product import Product
from typing import List

class ProductRepository(ABC):
    '''Интерфейс для работы с товарами'''
    @abstractmethod
    def get_product_data(self, url: str) -> Product:
        pass