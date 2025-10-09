from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import Product


class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        '''
        Сохраняет или обновляет продукт в репозитории.

        :param product: Объект типа Product, который нужно сохранить или обновить.
        :return: None
        '''
        pass

    @abstractmethod
    def get(self, product_id: str) -> Optional['Product']:
        '''
        Получает продукт по идентификатору.

        :param product_id: Идентификатор продукта.
        :return: Объект Product, если найден, иначе None.
        '''
        pass

    @abstractmethod
    def get_all(self, user_id: str) -> Optional[List['Product']]:
        '''
        Получает все продукты пользователя.

        :param user_id: Идентификатор пользователя, чьи продукты нужно получить.
        :return: Список объектов Product для данного пользователя.
        '''
        pass

    @abstractmethod
    def delete(self, product_id: str) -> bool:
        '''
        Удаляет продукт по идентификатору.

        :param product_id: Идентификатор продукта, который нужно удалить.
        :return: Возвращает True, если продукт был удалён, иначе False.
        '''
        pass

