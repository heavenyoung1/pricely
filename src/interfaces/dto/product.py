from pydantic import BaseModel, HttpUrl
from typing import List

from src.domain.entities import Product


class ProductCreateDTO(BaseModel):
    id: str
    user_id: str
    name: str
    link: HttpUrl
    image_url: HttpUrl
    rating: float
    categories: List[str]

    def to_domain(self) -> Product:
        return Product(
            id=self.id,
            user_id=self.user_id,
            price_id='',  # заполнит UseCase
            name=self.name,
            link=str(self.link),
            image_url=str(self.image_url),
            rating=self.rating,
            categories=self.categories,
        )