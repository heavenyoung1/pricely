from pydantic import BaseModel
from typing import List

from src.domain.entities import User


class UserDTO(BaseModel):
    id: str
    username: str
    chat_id: str
    products: List[str] = []

    def to_domain(self) -> User:
        return User(
            id=self.id,
            username=self.username,
            chat_id=self.chat_id,
            products=self.products
        )