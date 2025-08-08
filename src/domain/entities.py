from dataclasses import dataclass, field
from datetime import datetime
from typing import List

# Здесь — чистые классы, без Pydantic, ORM и инфраструктурных зависимостей

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


@dataclass
class Price:
    id: str
    product_id: str
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int
    default: int
    claim: datetime


@dataclass
class User:
    id: str
    username: str
    chat_id: str
    products: List[str] = field(default_factory=list)  # В домене как список