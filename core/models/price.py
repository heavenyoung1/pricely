from dataclasses import dataclass
from datetime import datetime

@dataclass
class Price:
    id: str
    product_id: str
    price: int
    timestamp: datetime 