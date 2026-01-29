from abc import ABC, abstractmethod
from typing import List, Dict

from domain.entities.user_products import UserProducts


class IUserProductsRepository(ABC):
    @abstractmethod
    async def save(self, user_id: int, product_id: int) -> UserProducts:
        '''Сохранить связь пользователь-товар'''
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: int) -> List[int]:
        '''Получить все товары пользователя (список ID товаров)'''
        pass

    @abstractmethod
    async def delete(self, user_id: int, product_id: int) -> bool:
        '''Удалить связь пользователь-товар'''
        pass

    @abstractmethod
    async def get_all_grouped(self) -> Dict[int, List[int]]:
        '''Получить сгруппированные данные: словарь {user_id: [product_ids]}'''
        pass
