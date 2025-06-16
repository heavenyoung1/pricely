from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    id: int
    url: str
    name: str
    price: int
    lastUpdated: datetime

    def updatePrice(self, )


