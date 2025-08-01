from pydantic.dataclasses import dataclass
from datetime import datetime
from pydantic import ConfigDict
from typing import List

from src.infrastruture.database.models.product import DBProduct

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

    def to_orm(self) -> 'DBProduct':
        from src.infrastruture.database.models.product import DBProduct  # Ленивый импорт
        return DBProduct(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            rating=self.rating,
            price_with_card=self.price_with_card,
            price_without_card=self.price_without_card,
            price_default=self.price_default,
            link=self.link,
            url_image=self.url_image,
            category_product=self.category_product,
            timestamp=self.timestamp
        )