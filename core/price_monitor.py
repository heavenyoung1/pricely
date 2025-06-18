import random
import time
from typing import Dict

from adapters.interfaces import IMarketPlace, ICache, INotifier


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
        attempts = self.attempts.get(url, 0)
        max_interval = 24 * 3600  # 24 часа
        while True:
            try:
                product = self.parser.parse_product(url)
                old_price = self.cache.get_price(url)
                if old_price is not None and old_price != product.price:
                    import asyncio
                    asyncio.run(self.notifier.notify(chat_id, product, old_price))
                self.cache.save_price(url, product.price)
                attempts = 0  # Сбрасываем попытки при успехе
            except Exception as e:
                attempts += 1
                print(f"Ошибка мониторинга {url}: {e}")
            # Экспоненциальный backoff с jitter
            sleep_time = min(self.interval * (2 ** attempts) + random.uniform(0, 100), max_interval)
            time.sleep(sleep_time)
            self.attempts[url] = attempts