from abc import ABC, abstractmethod
from typing import Dict

class ProductParser(ABC):
    '''
    Абстрактный интерфейс для парсеров продуктов.

    Этот интерфейс определяет методы для парсинга информации о товаре.
    '''
    
    @abstractmethod
    def parse_product(self, url: str) -> Dict:
        '''
        Парсит информацию о товаре по предоставленной ссылке.

        :param url: Ссылка на страницу товара.
        :return: Словарь с данными о товаре.
        '''
        pass
