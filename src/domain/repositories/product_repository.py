from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entitites import Product
from sqlalchemy.orm import Session

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        '''Сохранить или обновить товары.'''
        pass

    @abstractmethod
    def get(self, product_id: str) -> Product:
        '''Получить товар по ID.'''
        pass

    @abstractmethod
    def delete(self, product_id: str) -> None:
        '''Удалить товар из отслеживаемых'''
        pass

    @abstractmethod
    def get_all(self, user_id: str) -> Optional[List[Product]]:
        '''Получить все товары пользвателя по ID пользователя.'''
        pass