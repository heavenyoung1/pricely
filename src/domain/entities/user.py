from pydantic.dataclasses import dataclass, field_validator
from pydantic import ConfigDict

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

config = ConfigDict(strict=True, from_attributes=True,  arbitrary_types_allowed=True)

@dataclass(config=config)
class User:
    user_id: str
    username: str
    chat_id: str
    products: List['Product']

    # Конфиг для работы с ORM
    class Config:
        orm_mode = True  # Разрешает загрузку данных из ORM-объектов

    @field_validator('username')
    def validate_username(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Username не может быть пустым')
