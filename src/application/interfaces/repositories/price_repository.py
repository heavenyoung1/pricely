from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities import Price

class PriceRepository(ABC):
    '''
    Абстрактный репозиторий для работы с ценами.

    Этот интерфейс определяет методы для получения и управления ценами товаров.
    '''
    
    @abstractmethod
    def save(self, price: Price) -> None:
        '''
        Сохраняет или обновляет цену в репозитории.

        :param price: Объект типа Price, который нужно сохранить или обновить.
        :return: None
        '''
        pass

    @abstractmethod
    def get(self, price_id: str) -> Optional[Price]:
        '''
        Получает цену по идентификатору.

        :param price_id: Идентификатор цены.
        :return: Объект Price, если найден, иначе None.
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
    def delete(self, price_id: str) -> bool:
        '''
        Удалить цену по идентификатору.

        :param price_id: Идентификатор цены, которую нужно удалить.
        :return: Возвращает True, если цена была удалена, иначе False.
        '''
        pass

    @abstractmethod
    def get_latest_for_product(self, product_id: str) -> Optional[Price]:
        '''
        Получить последнюю цену для продукта по времени.

        :param product_id: Идентификатор продукта.
        :return: Объект Price, если цена найдена, иначе None.
        '''
        pass

    @abstractmethod
    def delete_all_prices_for_product(self, product_id: str) -> bool:
        '''
        Удалить все цены для товара по product_id.

        :param product_id: Идентификатор товара, для которого нужно удалить все связанные цены.
        :return: Возвращает True, если цены были удалены, иначе False.
        '''
        pass
