from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    id: int
    url: str
    name: str
    price: int
    last_updated: datetime

    def update_price(price: int):
        pass



