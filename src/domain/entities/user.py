from dataclasses import dataclass
from typing import List

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

@dataclass 
class User:
    user_id: str
    username: str
    chat_id: str
    products: List['Product']
