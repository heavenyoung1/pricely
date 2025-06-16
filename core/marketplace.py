from abc import ABC, abstractmethod
from models.product import Product

class IMarketPlace(ABC):
    @abstractmethod
    def parse_price(self, url: str) -> Product:
        pass
