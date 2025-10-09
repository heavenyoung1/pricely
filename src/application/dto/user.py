from pydantic import BaseModel
from typing import List

# УДАЛИТЬ ПОЗЖЕ
class UserDTO(BaseModel):
    id: str
    username: str
    chat_id: str
    products: List[str] = []