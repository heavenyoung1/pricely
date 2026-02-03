from dataclasses import dataclass
from core.logger import logger
from typing import List

from domain.exceptions import PriceNotFoundError

@dataclass
class UserProducts:
    user_id: int
    product_id: int

@dataclass
class UserProductsData:
    chat_id: int
    product_links: List[str]

@dataclass
class CheckedProduct:
    url: str
    price_with_card: int
    price_without_card: int

    @staticmethod
    def create(
        *,
        url: str,
        price_with_card: int,
        price_without_card: int,
    ) -> 'CheckedProduct':
        return CheckedProduct(
            url=url,
            price_with_card=price_with_card,
            price_without_card=price_without_card,
        )
    
    def __post_init__(self):
        '''Валидация и нормализация данных после создания'''
        if not isinstance(self.price_with_card, int):
            logger.error(f'Сканирование цен завершилось ошибкой: {self.url}')
            raise PriceNotFoundError(self.url)
        if not isinstance(self.price_without_card, int):
            logger.error(f'Сканирование цен завершилось ошибкой: {self.url}')
            raise PriceNotFoundError(self.url)