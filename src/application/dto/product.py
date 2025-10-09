from pydantic import BaseModel, HttpUrl
from typing import List

# УДАЛИТЬ ПОЗЖЕ
class ProductDTO(BaseModel):
    id: str
    user_id: str
    name: str
    link: HttpUrl
    image_url: HttpUrl
    rating: float
    categories: str
