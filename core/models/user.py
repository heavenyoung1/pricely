from dataclasses import dataclass
from typing import List

from core.models.product import Product

@dataclass
class User:
    id: str
    telegram_id: str
    products: List['Product'] = []

    def follow(self, product: Product) -> None:
        if product not in self.products:
            self.products.append(product)

    def unfollow(self, product: Product) -> None:
        self.products.remove(product)