from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# УДАЛИТЬ ПОЗЖЕ
class PriceDTO(BaseModel):
    id: Optional[int]  # 🔥 iвтоинкремент в БД
    product_id: str
    with_card: int
    without_card: int
    previous_with_card: Optional[int] = None  # Разрешаем None
    previous_without_card: Optional[int] = None  # Разрешаем None
    created_at: datetime