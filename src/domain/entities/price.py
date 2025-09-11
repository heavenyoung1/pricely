from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    id: int  # Автоинкрементный ID
    product_id: str  # Связь с продуктом
    with_card: int
    without_card: int
    previous_with_card: int | None
    previous_without_card: int | None
    default: int
    created_at: datetime  # Дата клейма цены