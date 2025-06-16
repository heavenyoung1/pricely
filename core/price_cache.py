from adapters.interfaces import ICache
from dataclasses import dataclass
from typing import Optional

@dataclass
class JSONPriceCache(ICache):
    def save_price(url: str, price: int) -> None:
        pass

    def get_price(url: str) -> Optional[int]:
        pass