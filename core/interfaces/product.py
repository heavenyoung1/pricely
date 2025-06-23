from abc import ABC, abstractmethod
from typing import Optional, List

from core.models.product import Product

class IProductRepo(ABC):
    @abstractmethod
    async def save(self, product: 'Product') -> None:
        pass

    @abstractmethod
    async def find_all(self) -> List['Product']:
        pass

    @abstractmethod
    async def find_by_url(self, url: str) -> Optional['Product']:
        pass