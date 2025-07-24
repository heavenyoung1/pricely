from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    '''Сущность Product (товар)'''
    id: str  # артикул
    name: str
    rating: float
    price_with_card: int
    price_without_card: int
    previous_price_without_card: int # Добавлено для отслеживания
    price_default: int
    discount_amount: float
    link: str
    url_image: str
    category_product: List[str]

