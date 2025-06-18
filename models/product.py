from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    id: str
    url: str
    name: str
    price: int
    last_updated: datetime

    def update_price(self, price: int) -> None:
        self.price = price
        self.last_updated = datetime.now()



