from dataclasses import dataclass
from core.logger import logger


@dataclass
class Product:
    id: int
    article: str
    name: str
    link: str
    change: int

    @staticmethod
    def create(
        *,
        article: str,
        name: str,
        link: str,
        change: int,
    ) -> 'Product':
        return Product(id=None, article=article, name=name, link=link, change=change)

    def __post_init__(self):
        '''Валидация и нормализация данных после создания'''

        if not isinstance(self.article, str):
            logger.error(f'Арткул не является типом string')
            raise ValueError()

        if not isinstance(self.name, str):
            logger.error(f'Название товара не является типом string')
            raise ValueError()


@dataclass
class FullProduct:
    id: int
    article: str
    name: str
    link: str

    price_with_card: int
    price_without_card: int
    price_previous_with_card: int
    price_previous_without_card: int

    change: int
