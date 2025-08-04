from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.infrastructure.database.models.price_stamp import DBPriceStamp

# Strict Mode - Строгий режим, запрещающий конвертацию типов 
# (500.0 -> 500 || float -> int) - подобное поведение ЗАПРЕЩЕНО
config = ConfigDict(strict=True)

@dataclass(config=config)
class PriceStamp:
    '''Сущность - Клейм Цены'''
    ID_stamp: str                       # ID клейма 
    ID_product: str                     # ID продукта 
    time_stamp: datetime                # Время клейма 
    price_with_card: int
    price_without_card: int
    previous_price_with_card: int
    previous_price_without_card: int
    price_default: int

    def to_orm(self) -> 'DBPriceStamp':
        from src.infrastructure.database.models.price_stamp import DBPriceStamp
        return DBPriceStamp(
            ID_stamp=self.ID_stamp,
            ID_product=self.ID_product,
            time_stamp=self.time_stamp,
            price_with_card=self.price_with_card,
            price_without_card=self.price_without_card,
            previous_price_with_card=self.previous_price_with_card,
            previous_price_without_card=self.previous_price_without_card,
            price_default=self.price_default,
        )
