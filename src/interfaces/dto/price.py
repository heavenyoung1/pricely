from pydantic import BaseModel
from datetime import datetime


class PriceDTO(BaseModel):
    id: str
    product_id: str
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int
    default: int
    claim: datetime