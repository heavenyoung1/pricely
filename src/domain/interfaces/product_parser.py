from abc import ABC, abstractmethod

class IProductParser(ABC):
    @abstractmethod
    def parse_product(self, url: str) -> dict:
        '''Парсит продукт по ссылке и возвращает словарь с данными'''
        pass