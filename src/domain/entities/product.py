from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Product:
    id: str  # Артикул из 10 цифр
    user_id: str  # Связь с пользователем (заполняется в UseCase)
    price_id: str  # Связь с ценой (заполняется в UseCase)
    name: str
    link: str
    image_url: str
    rating: float
    categories: List[str]