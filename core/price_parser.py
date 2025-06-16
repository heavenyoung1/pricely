from models.product import Product
from typing import Optional

class PriceParser():
    def __init__(self, adapter: str):
        self.adapter = adapter

    def parse(self, url: str, markerplace: str) -> Product:
        pass