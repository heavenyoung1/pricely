from abc import ABC, abstractmethod
from typing import Optional, List
from .entities import Product, Price, User
from sqlalchemy.orm import Session

# Доменный слой описывает контракты, инфраструктура реализует

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        '''Сохранить или обновить товары.'''
        pass

    @abstractmethod
    def get_product(self, product_id: str) -> Product:
        '''Получить товар по ID.'''
        pass

    @abstractmethod
    def delete_product(self, product_id: str) -> None:
        '''Удалить товар из отслеживаемых'''
        pass

    @abstractmethod
    def get_all_product(self, user_id: str) -> Optional[List[Product]]:
        '''Получить все товары пользвателя по ID пользователя.'''
        pass

# ----- # ----- # ----- # ----- # ----- # ----- # ----- #

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

# ----- # ----- # ----- # ----- # ----- # ----- # ----- #

class UserRepository(ABC):
    @abstractmethod
    def save_user(self, user: User) -> None:
        '''Сохранить или обновить пользователя.'''
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        '''Получить пользователя по ID.'''
        pass

# ----- # ----- # ----- # ----- # ----- # ----- # ----- #