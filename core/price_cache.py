import os
import json

from dataclasses import dataclass
from typing import Optional, Dict

from adapters.interfaces import ICache


@dataclass
class JSONPriceCache(ICache):
    cache_file: str
    cache: Dict[str, int] = None

    def __post_init__(self) -> None:
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict[str, int]:
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_price(self, url: str, price: int) -> None:
        self.cache[url] = price
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def get_price(self, url: str) -> Optional[int]:
        return self.cache.get(url)