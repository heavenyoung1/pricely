from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import Product


class UserProductsRepository(ABC):
    @abstractmethod
    def get_products_for_user(self, user_id: str) -> None:
        '''
        Получить все товары пользователя
        
        Raises:
            DatabaseError: При ошибках работы с БД
            ValueError: При невалидных данных товара
        '''
        pass