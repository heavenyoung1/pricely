from abc import ABC, abstractmethod

from domain.entities.product import Product
 
class ProductParser(ABC):
    """Интерфейс для парсинга данных о продукте."""
    
    @abstractmethod
    def parse_product(self, url: str) -> Product:
        pass