from adapters.interfaces import IMarketplace, INotifier, ICache
from models.product import Product
import time
import random
from typing import Dict






class PriceMonitor:
    def __init__(
            self,
            parser: IMarketplace,
            cache: ICache,
            notifier: INotifier,
            interval: int = 3600,
    ):
        self.parser = parser
        self.cache = cache
        self.notifier = notifier
        self.interval = interval
        self.attempts: Dict[str, int] = {}

    def monitors(self, url: str, chat_id: int) -> None:
        attempts = self.attempts.get(url, 0)
        max_interval = 24 * 3600 # 24 hours

        product = self.parser.parse_product