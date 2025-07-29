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