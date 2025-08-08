from pydantic import BaseModel, HttpUrl
from typing import List
from datetime import datetime

class ProductCreateDTO(BaseModel):
    id: str
    user_id: str
    name: str
    link: HttpUrl
    image_url: HttpUrl
    rating: float
    categories: List[str]

class PriceCreateDTO(BaseModel):
    id: str
    product_id: str
    with_card: int
    without_card: int
    previous_with_card: int
    previous_without_card: int
    default: int
    claim: datetime

class UserCreateDTO(BaseModel):
    id: str
    username: str
    chat_id: str
    products: List[str] = []