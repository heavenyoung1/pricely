from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class PriceStamp:
    '''Сущность - Клейм Цены'''
    ID_stamp: int                       # ID клейма 
    ID_product: str                     # ID продукта 
    time_stamp: datetime                # Время клейма 
    price_with_card: int
    price_without_card: int
    previous_price_with_card: int
    previous_price_without_card: int
    price_default: int

    # def to_orm(self, product_id: str) -> DBPriceStamp:
    #     return DBPriceStamp(
    #         ID_product=product_id,
    #         time_stamp=self.time_stamp,
    #         price_with_card=self.price_with_card,
    #         price_without_card=self.price_without_card,
    #         previous_price_without_card=self.previous_price_without_card,
    #         price_default=self.price_default
    #     )