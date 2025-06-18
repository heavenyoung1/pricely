import asyncio
import random
import time
from typing import Dict

from adapters.interfaces import IMarketPlace, ICache, INotifier
from models.product import Product


class PriceMonitor:
    def __init__(
        self,
        parser: IMarketPlace,
        cache: ICache,
        notifier: INotifier,
        interval: int = 3600,
    ):
        self.parser = parser
        self.cache = cache
        self.notifier = notifier
        self.interval = interval
        self.attempts: Dict[str, int] = {}

    def monitor(self, url: str, chat_id: int) -> None:
        """Continuously monitor the price of a product and notify on changes."""
        attempts = self.attempts.get(url, 0)
        max_interval = 24 * 3600  # 24 hours
        while True:
            try:
                product = self.parser.parse_product(url)
                old_price = self.cache.get_price(url)
                if old_price is not None and old_price != product.price:
                    asyncio.run(self.notifier.notify(chat_id, product, old_price))
                self.cache.save_price(url, product.price)
                attempts = 0  # Reset attempts on success
            except Exception as e:
                attempts += 1
                print(f"Monitoring error {url}: {e}")
            # Exponential backoff with jitter
            sleep_time = min(self.interval * (2**attempts) + random.uniform(0, 100), max_interval)
            time.sleep(sleep_time)
            self.attempts[url] = attempts

    async def check_once(self, url: str, chat_id: int) -> None:
        """Check the product price once and notify if it has changed."""
        try:
            product = self.parser.parse_product(url)
            old_price = self.cache.get_price(url)
            if old_price is not None and old_price != product.price:
                await self.notifier.notify(chat_id, product, old_price)
            self.cache.save_price(url, product.price)
            self.attempts[url] = 0
        except Exception:
            self.attempts[url] = self.attempts.get(url, 0) + 1