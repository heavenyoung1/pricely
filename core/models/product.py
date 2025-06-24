from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from typing import Dict, Optional

from core.models.price import Price

@dataclass
class ProductInfo:
    id: str
    name: str
    url: str
    last_price: float
    image_url: Optional[str]

@dataclass
class Product:
    id: str
    name: str
    url: str
    marketplace: str # Оптимизировать
    last_price: int
    image_url: str # Опциональоно

    def update_price(self, new_price: int) -> Dict:
        changed: bool = self.last_price != new_price
        result = {
            'changed': changed,
            'last_price': self.last_price,
            'new_price': new_price,
        }

        if changed:
            self.last_price = new_price
        return result
    
    def make_price_record(self) -> Price:
        return Price(
            id=str(uuid4()),
            product_id=self.id,
            price=self.last_price,
            timestamp=datetime.now()
    )

