from abc import ABC, abstractmethod
from typing import Dict

class ParserError(Exception):
    '''Исключение для ошибок парсинга данных с маркетплейсов.'''
    pass

class Parser(ABC):
    '''Интерфейс для парсера товаров с маркетплейсов.

    Этот класс предоставляет базовые методы для парсинга страницы товара и извлечения нужных данных.
    Все парсеры должны реализовывать метод `parse_product` для извлечения информации о товаре по его URL.
    '''
    
    @abstractmethod
    def parse_product(self, url: str) -> Dict:
        '''Парсит страницу товара по URL и возвращает данные.

        Args:
            url (str): URL страницы товара.
            
        Returns:
            Dict: Словарь с данными (name, id, url, and etc.).
        
        Raises:
            ParserError: Если парсинг не удался (например, из-за некорректного формата страницы).
        '''
        pass
