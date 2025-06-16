from adapters.ozon_adapter import OzonAdapter
from adapters.wb_adapter import WBAdapter

from core.price_parser import PriceParser
from core.price_monitor import PriceMonitor
from core.price_cache import JSONPriceCache



class PriceTracker:
    def __init__(
                self,
                bot_token: str,
                driver_path: str,
                cache_file: str = 'prices.json',
                interval: int = 3600,
    ):
        adapters = {
              'ozon': OzonAdapter(driver_path),
              'wb': WBAdapter(driver_path),
        }

        self.parser = PriceParser(adapters)
        cache = JSONPriceCache(cache_file)
        notifier = None # тут будет notifier
        self.monitor = PriceMonitor(self.parser, cache, notifier, interval)

    def add_product(self, url: str, marketplace: str) -> None:
        product = self.parser.parse(url, marketplace)
        self.monitor.cache.save_price(url, product.price)
        return product

    def monitor_price(self, url: str, chat_id: int, marketplace: str) -> None:
        self.monitor.monitor(url, chat_id)