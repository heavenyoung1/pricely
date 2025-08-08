from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.entities import Product


class ProductRepository(ABC):
    @abstractmethod
    def save_product(self, product: Product) -> None:
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

    # @abstractmethod
    # def find_product_by_id(self, product_id: str) -> Optional[Product]:
    #     pass

    @abstractmethod
    def get_all_product(self, user_id: str) -> Optional[List[Product]]:
        '''Получить все товары пользвателя по ID пользователя.'''
        pass
