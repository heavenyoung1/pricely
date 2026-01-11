from abc import ABC, abstractmethod
from typing import Optional

from src.domain.enttities.product import Product


class IProductRepository(ABC):
    @abstractmethod
    async def save(self, product: Product) -> Product:
        '''Сохранить товар'''
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[Product]:
        '''Получить товар по ID'''
        pass

    @abstractmethod
    async def update(self, product: Product) -> Product:
        '''Обновить товар'''
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        '''Удалить товар по ID'''
        pass
