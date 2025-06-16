from models.product import Product
from typing import Optional
from adapters.interfaces import IMarketPlace

class PriceParser():
    def __init__(self, adapter: dict[str, IMarketPlace]):
        self.adapter = adapter

    def parse(self, url: str, markerplace: str) -> Product:
        pass