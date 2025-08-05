from pydantic import BaseModel, HttpUrl, field_validator, ConfigDict
from typing import List, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from .price_claim import PriceClaim

# Strict Mode - Строгий режим, запрещающий конвертацию типов 
config = ConfigDict(strict=True)

class Product(BaseModel):
    '''Сущность - товар'''
    product_id: str
    user_id: str
    name: str
    link: HttpUrl
    image_url: HttpUrl
    rating: float
    categories: List[str]
    price_stamps: List['PriceClaim']

    model_config = ConfigDict(
        strict=True,
        from_attributes=True  # Разрешает загрузку данных из ORM-объектов
    )