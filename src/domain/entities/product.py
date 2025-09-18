from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from . import Price

@dataclass
class Product:
    id: str  # Артикул из 10 цифр
    user_id: str  # Связь с пользователем (заполняется в UseCase)
    name: str
    link: str
    image_url: str
    rating: float
    categories: str
    prices: List['Price'] = field(default_factory=list)

    @property
    def latest_price(self) -> Optional['Price']:
        if not self.prices:
            return None
        # Сортируем по created_at (убывание) и id (убывание) для выбора последней цены
        return max(self.prices, key=lambda p: (p.created_at or datetime.min, p.id or '0'))