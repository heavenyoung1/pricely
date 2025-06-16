from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class PriceHistory:
    id: str
    url: str
    history: List[Tuple[int, float]]

    def add_price(price: int):
        pass

    def get_last_price():
        pass

