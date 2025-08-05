from pydantic.dataclasses import dataclass
from pydantic import ConfigDict

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product

config = ConfigDict(strict=True)

@dataclass(config=config)
class User:
    user_id: str
    username: str
    chat_id: str
    products: List['Product']
