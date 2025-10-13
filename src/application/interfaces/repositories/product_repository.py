from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import Product

class ProductRepository(ABC):
    '''
    Абстрактный репозиторий для работы с продуктами.

    Этот интерфейс определяет методы для получения, сохранения и удаления товаров.
    '''
    
    @abstractmethod
    def save(self, product: Product) -> None:
        '''
        Сохраняет или обновляет продукт в репозитории.

        :param product: Объект типа Product, который нужно сохранить или обновить.
        :return: None
        '''
        pass

    @abstractmethod
    def get(self, product_id: str) -> Optional[Product]:
        '''
        Получает товар по идентификатору.

        :param product_id: Идентификатор продукта.
        :return: Объект Product, если найден, иначе None.
        '''
        pass

    @abstractmethod
    def get_all(self, user_id: str) -> List[Product]:
        '''
        Получает все товары пользователя.

        :param user_id: Идентификатор пользователя, чьи товары нужно получить.
        :return: Список объектов Product для данного пользователя.
        '''
        pass

    @abstractmethod
    def delete(self, product_id: str) -> bool:
        '''
        Удаляет товар по идентификатору.

        :param product_id: Идентификатор товара, который нужно удалить.
        :return: Возвращает True, если товар был удален, иначе False.
        '''
        pass
