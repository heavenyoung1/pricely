from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List

class Product(BaseModel):
    '''Сущность - товар'''
    id: str
    user_id: str
    price_id: str
    name: str
    link: HttpUrl
    image_url: HttpUrl
    rating: float
    categories: List[str]

    model_config = ConfigDict(
        strict=True,
        from_attributes=True  # Разрешает загрузку данных из ORM-объектов
    )