from dataclasses import dataclass, field
from typing import List

from core.models.product import Product

@dataclass
class User:
    id: str
    telegram_id: str
    products: List['Product'] = field(default_factory=list)

    def subscribe(self, product: Product) -> None:
        if product not in self.products:
            self.products.append(product)

    def unsubscribe(self, product: Product) -> None:
        self.products.remove(product)