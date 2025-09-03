from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import Price
from sqlalchemy.orm import Session

class PriceRepository(ABC):
    @abstractmethod
    def save(self, price: Price) -> None:
        '''Сохранить или обновить цену.'''
        pass

        # ПО МОЕМУ ЭТО ЗДЕСЬ ЛИШНЕЕ, ЕГО НУЖНО В ДРУГОЙ РЕПОЗИТОРИЙ ПЕРЕНЕСТИ!
    # @abstractmethod
    # def get_relevant_price_id(self, product_id: str) -> Optional[str]:
    #     '''Получить ID актуальной цены по ID продукта.'''
    #     pass

    @abstractmethod
    def get(self, price_id: str) -> Optional[Price]:
        '''Получить цену по ID.'''
        pass

    @abstractmethod
    def get_all_prices_by_product(self, product_id: str) -> List[Price]:
        '''Получить все цены для продукта.'''
        pass
    
    @abstractmethod
    def delete(self, price_id: str) -> None:
        '''Удалить цену по ID.'''
        pass