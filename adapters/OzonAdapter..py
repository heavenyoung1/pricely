from adapters.interfaces import IMarketPlace
from dataclasses import dataclass
from models.product import Product

@dataclass
class OzonAdapter(IMarketPlace):
    def parse_product(url: str) -> Product:
        pass