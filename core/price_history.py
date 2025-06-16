from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Optional


@dataclass
class PriceHistory:
    id: str
    url: str
    history: List[Tuple[int, datetime]]

    def add_price(self, price: int) -> None:
        self.history.append((price, datetime.now()))

    def get_last_price(self) -> Optional[int]:
        return self.history[-1] if self.history else None #return self.history[-1][0] if self.history else None

