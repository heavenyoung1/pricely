from abc import ABC, abstractmethod
from models.product import Product
from typing import Optional

class IMarketPlace(ABC):

    @abstractmethod
    def _get_id(self, url: str) -> str:
        pass

    @abstractmethod
    def parse_product(self, url: str) -> Product:
        pass

class INotifier(ABC):
    @abstractmethod
    def notify(self, chat_id: int, product: Product, old_price: int) -> None:
        pass

class ICache(ABC):
    @abstractmethod
    def save_price(self, url: str, price: int) -> None:
        pass

    @abstractmethod
    def get_price(self, url: str) -> Optional[int]:
        pass
