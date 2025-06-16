from models.product import Product
from typing import Optional
from adapters.interfaces import IMarketPlace

class PriceParser():
    def __init__(self, adapters: dict[str, IMarketPlace]):
        self.adapters = adapters

    def parse(self, url: str, marketplace: str) -> Product:
        adapter = self.adapters.get(marketplace)
        return adapter.parse_product(url)