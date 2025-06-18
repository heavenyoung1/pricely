from adapters.ozon_adapter import OzonAdapter
from adapters.wb_adapter import WBAdapter
from models.product import Product

from core.price_parser import PriceParser
from core.price_monitor import PriceMonitor
from core.price_cache import JSONPriceCache



class PriceTracker:
    def __init__(self, driver_path: str, cache_file: str, interval: int):
        self.parser = PriceParser(driver_path=driver_path)
        self.monitor = PriceMonitor(
            parser=self.parser,
            cache=cache_file,  # Предполагается ICache
            notifier=None,  # Нет Telegram, возможно, None или другой INotifier
            interval=interval
        )

    def add_product(self, url: str, marketplace: str) -> Product:
            product = self.parser.parse(url, marketplace)
            self.monitor.cache.save_price(url, product.price)
            return product

    def monitor_price(self, url: str, chat_id: int, marketplace: str) -> None:
            self.monitor.monitor(url, chat_id)