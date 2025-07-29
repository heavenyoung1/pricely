from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp

class ProductRepository(ABC):
    @abstractmethod
    def save_one_product(self, product: Product, price_stamp: PriceStamp) -> None:
        pass

    @abstractmethod
    def save_few_products(self, products: List[Product], price_stamp: PriceStamp) -> None:
        pass

    @abstractmethod
    def find_product_by_url(self, product_url: str) -> Optional[Product]:
        pass

    @abstractmethod
    def find_product_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def find_few_products(self) -> List[Product]:
        pass