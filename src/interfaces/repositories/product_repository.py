from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities import Product


class ProductRepository(ABC):
    @abstractmethod
    def save_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def find_product_by_url(self, product_url: str) -> Optional[Product]:
        pass

    @abstractmethod
    def find_product_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def find_all_products_for_user(self, user_id: str) -> Optional[List[Product]]:
        pass

    @abstractmethod
    def delete_product(self, product_id: str) -> None:
        pass