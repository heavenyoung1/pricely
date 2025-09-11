from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PriceDTO(BaseModel):
    id: str
    product_id: str
    with_card: int
    without_card: int
    previous_with_card: Optional[int] = None  # Разрешаем None
    previous_without_card: Optional[int] = None  # Разрешаем None
    default: int
    created_at: datetime