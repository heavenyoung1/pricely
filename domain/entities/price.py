from dataclasses import dataclass
from core.logger import logger

@dataclass
class Price:
    id: int
    product_id: int
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int

    @staticmethod
    def create(
        *,
        product_id: str,
        with_card: int,
        without_card: int,
        previous_with_card: int,
        previous_without_card: int,
    ) -> 'Price':
        return Price(
            id=None,
            product_id=product_id,
            with_card=with_card,
            without_card=without_card,
            previous_with_card=previous_with_card,
            previous_without_card=previous_without_card,
        )

    def __post_init__(self):
        '''Валидация и нормализация данных после создания'''

        # Валидация цены
        if not isinstance(self.with_card, int) or not isinstance(self.without_card, int):
            logger.error(f'Полученная при парсинге цена не является типом INTEGER')
            raise ValueError()