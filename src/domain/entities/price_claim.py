from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .price import Price

class PriceClaim(BaseModel):
    '''Сущность - клейм Цены'''
    claim_id: str
    product_id: str
    time_claim: datetime
    price: Price

    model_config = ConfigDict(
    strict=True,
    from_attributes=True
    )

    @field_validator('with_card', 'without_card', 'previous_with_card', 'previous_without_card', 'default')
    def validate_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError('Ошибка считвания цены, значение < 0.')
        return value