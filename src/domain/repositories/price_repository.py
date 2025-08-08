from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import Price
from sqlalchemy.orm import Session

class PriceRepository(ABC):

    @abstractmethod
    def save(self, price: Price) -> None:
        '''Сохранить или обновить цену.'''
        pass

    @abstractmethod
    def get(self, price_id: str) -> Price:
        '''Получить цену по ID.'''
        pass

    @abstractmethod
    def get_prices_by_product(self, product_id: str) -> list[Price]:
        '''Получить все цены для продукта.'''
        pass