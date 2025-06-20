from dataclasses import dataclass
from uuid import uuid4
from typing import List

@dataclass
class User:
    id: uuid4
    telegram_id: str
    products: List


    def follow(product):
        pass

    def unfollow(product):
        pass