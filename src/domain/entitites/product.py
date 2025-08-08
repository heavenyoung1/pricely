from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    id: str
    user_id: str
    price_id: str
    name: str
    link: str
    image_url: str
    rating: float
    categories: List[str]