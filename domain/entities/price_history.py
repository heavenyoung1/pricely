from dataclasses import dataclass
from datetime import datetime

@dataclass
class PriceHistory:
    '''История изменения цены товара'''
    id: str  # артикул
    product_id: str
    price_with_card: int
    price_without_card: int
    previous_price_without_card: int # Добавлено для отслеживания
    price_default: int
    timestamp: datetime