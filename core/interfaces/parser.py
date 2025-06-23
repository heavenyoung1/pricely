from abc import ABC, abstractmethod

from core.models.product import Product

class IProductParser(ABC):
    @abstractmethod
    def parse(self, url: str) -> Product:
        pass