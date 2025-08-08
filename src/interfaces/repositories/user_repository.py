from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

from src.domain.entities.product import Product

if TYPE_CHECKING:
    from src.domain.entities import Price

class UserRepository(ABC):
    @abstractmethod
    def save_price_stamp(self, product: Product, price: Price):
        pass