from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .price_claim import PriceClaim

# Strict Mode - Строгий режим, запрещающий конвертацию типов 
config = ConfigDict(strict=True)

@dataclass(config=config)
class Product:
    '''Сущность Product (товар)'''
    product_id: str
    user_id: str
    name: str
    link: str
    image_url: str
    rating: float
    categories: List[str]
    price_stamps: List['PriceClaim']