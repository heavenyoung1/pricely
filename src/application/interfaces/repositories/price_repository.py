from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import Price

class PriceRepository(ABC):
    @abstractmethod
    def save(self, price: Price) -> None:
        '''
        Сохранить или обновить цену в репозитории.

        :param price: Объект типа Price, который необходимо сохранить.
        :return: None
        '''
        pass

    @abstractmethod
    def get(self, price_id: str) -> Optional[Price]:
        '''
        Получить цену по идентификатору.

        :param price_id: Идентификатор цены.
        :return: Возвращает объект Price, если он найден, иначе None.
        '''
        pass

    @abstractmethod
    def get_all_prices_by_product(self, product_id: str) -> List[Price]:
        '''
        Получить все цены для конкретного продукта.

        :param product_id: Идентификатор продукта.
        :return: Список объектов Price для данного продукта.    
        '''
        pass
    
    @abstractmethod
    def delete(self, price_id: str) -> None:
        '''
        Удалить цену по идентификатору.

        :param price_id: Идентификатор цены.
        :return: None
        '''
        pass

    def get_latest_for_product(self, product_id: str) -> Price | None:
        '''
        Получить последнюю цену для продукта по времени.

        :param product_id: Идентификатор продукта.
        :return: Объект Price, если цена найдена, иначе None.
        '''
        pass