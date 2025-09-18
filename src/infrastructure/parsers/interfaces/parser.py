from abc import ABC, abstractmethod
from typing import Dict, Optional

class ParserError(Exception):
    '''Исключение для ошибок парсинга.'''
    pass

class Parser(ABC):
    '''Интерфейс для парсера товаров с маркетплейсов.'''
    
    @abstractmethod
    def parse_product(self, url: str) -> Dict:
        '''Парсит страницу товара по URL и возвращает данные.
        
        Args:
            url (str): URL страницы товара
            
        Returns:
            Dict: Словарь с данными (title, price, image, и т.д.)
        
        Raises:
            ParserError: Если парсинг провалился
        '''
        pass