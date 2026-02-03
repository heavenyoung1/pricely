from abc import ABC, abstractmethod
from typing import List

from domain.entities.user_products import ParsedProduct, CheckedPrice


class IProductParser(ABC):
    '''
    Интерфейс парсера товаров.
    Определяет контракт для извлечения данных со страниц магазина.
    '''

    @abstractmethod
    async def parse_new_product(self, url: str) -> ParsedProduct:
        '''
        Парсит страницу товара для добавления в систему.

        Args:
            url: URL страницы товара.

        Returns:
            ParsedProduct с полными данными о товаре.
        '''
        pass

    @abstractmethod
    async def fetch_current_prices(self, urls: List[str]) -> List[CheckedPrice]:
        '''
        Парсит текущие цены для списка товаров.

        Args:
            urls: Список URL страниц товаров.

        Returns:
            Список CheckedPrice с актуальными ценами.
        '''
        pass
