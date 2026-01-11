from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.price import Price


class IPriceRepository(ABC):
    @abstractmethod
    async def save(self, price: Price) -> Price:
        '''Сохранить цену'''
        pass

    @abstractmethod
    async def get_actual(self, product_id: int) -> Optional[Price]:
        '''Получить актуальную (последнюю) цену для товара'''
        pass

    @abstractmethod
    async def get_all_by_product(self, product_id: int) -> List[Price]:
        '''Получить все цены для товара'''
        pass

    @abstractmethod
    async def delete_by_product(self, product_id: int) -> int:
        '''Удалить все цены для товара. Возвращает количество удаленных записей'''
        pass
