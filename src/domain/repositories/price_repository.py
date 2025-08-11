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
    def get_relevant_price_id(self, product_id: str) -> Optional[str]:
        '''Получить ID актуальной цены по ID продукта.'''
        pass

    @abstractmethod
    def get(self, price_id: str) -> Optional[Price]:
        '''Получить цену по ID.'''
        pass

    @abstractmethod
    def get_prices_by_product(self, product_id: str) -> List[Price]:
        '''Получить все цены для продукта.'''
        pass

    @abstractmethod
    def delete(self, price_id: str) -> None:
        '''Удалить цену по ID.'''
        pass

    @abstractmethod
    def get_all(self, user_id: str) -> List[Price]:
        '''Получить все цены для пользователя по ID.'''
        pass