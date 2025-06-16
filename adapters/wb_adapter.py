from adapters.interfaces import IMarketPlace
from dataclasses import dataclass
from models.product import Product

@dataclass
class WBAdapter(IMarketPlace):
    def parse_product(url: str) -> Product:
        pass