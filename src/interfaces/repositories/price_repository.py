from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities import Price

class PriceRepository(ABC):
    @abstractmethod
    def save_price(self, price: Price) -> None:
        '''Сохранить или обновить цену.'''
        pass

    @abstractmethod
    def get_price(self, price_id: str) -> Price:
        '''Получить цену по ID.'''
        pass

    @abstractmethod
    def get_prices_by_product(self, product_id: str) -> list[Price]:
        '''Получить все цены для продукта.'''
        pass