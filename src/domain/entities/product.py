from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, field_validator, HttpUrl
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
    link: HttpUrl
    image_url: HttpUrl
    rating: float
    categories: List[str]
    price_stamps: List['PriceClaim']

    @field_validator('rating')
    def validate_raiting(cls, value: float) -> float:
        if not 0 <= value <= 5:
            raise ValueError('Рейтинг должен быть от 0 до 5')
        return value