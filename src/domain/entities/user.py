from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    id: str
    username: str
    chat_id: str
    products: List[str]  # Список идентификаторов продуктов (через user_products)