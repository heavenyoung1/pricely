from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import Product


class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        '''
        Сохранить или обновить товар.
        
        Raises:
            DatabaseError: При ошибках работы с БД
            ValueError: При невалидных данных товара
        '''
        pass

    @abstractmethod
    def get(self, product_id: str) -> Optional['Product']:
        '''
        Найти продукт по ID.
        
        Args:
            product_id: Идентификатор продукта
            
        Returns:
            Optional[Product]: Найденный продукт или None
        '''
        pass

    @abstractmethod
    def get_all(self, user_id: str) -> Optional[List['Product']]:
        '''
        Получить все продукты пользователя.
        
        Args:
            user_id: Идентификатор пользователя
            
        Returns:
            List[Product]: Список продуктов (пустой, если нет продуктов)
        '''
        pass

    @abstractmethod
    def delete(self, product_id: str) -> bool:
        '''
        Удалить продукт по ID.
        
        Args:
            product_id: Идентификатор продукта
            
        Returns:
            bool: True если удаление успешно, False если продукт не найден
        '''
        pass

