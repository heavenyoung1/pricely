from pydantic.dataclasses import dataclass
from pydantic import ConfigDict
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .price import Price

# Strict Mode - Строгий режим, запрещающий конвертацию типов 
# (500.0 -> 500 || float -> int) - подобное поведение ЗАПРЕЩЕНО
config = ConfigDict(strict=True)

@dataclass(config=config)
class PriceClaim:
    '''Сущность - Клейм Цены'''
    claim_id: str
    product_id: str
    time_claim: datetime
    price: Price