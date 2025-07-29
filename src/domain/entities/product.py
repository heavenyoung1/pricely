#from dataclasses import dataclass
from pydantic.dataclasses import dataclass
from datetime import datetime
from pydantic import ConfigDict
from typing import List

# Strict Mode - Строгий режим, запрещающий конвертацию типов 
# (500.0 -> 500 || float -> int) - подобное поведение ЗАПРЕЩЕНО
config = ConfigDict(strict=True)

@dataclass(config=config)
class Product:
    '''Сущность Product (товар)'''
    id: str
    user_id: str
    name: str
    rating: float
    price_with_card: int
    price_without_card: int
    previous_price_with_card: int
    previous_price_without_card: int
    price_default: int
    #discount_amount: float
    link: str
    url_image: str
    category_product: List[str]
    timestamp: datetime