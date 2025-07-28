from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product, price_stamp: PriceStamp) -> None:
        pass

    @abstractmethod
    def find_by_url(self, product_url: str) -> Optional[Product]:
        pass