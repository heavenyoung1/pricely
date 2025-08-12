from pydantic import BaseModel, HttpUrl
from typing import List


class ProductDTO(BaseModel):
    id: str
    user_id: str
    name: str
    link: HttpUrl
    image_url: HttpUrl
    rating: float
    categories: List[str]
