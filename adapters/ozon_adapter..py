from adapters.interfaces import IMarketPlace
from dataclasses import dataclass
from models.product import Product

@dataclass
class OzonAdapter(IMarketPlace):

    def extract_product_id(url: str) -> str:
        splitedStr = url.split("/")[-2]
        ID = splitedStr[-10:]
        return ID

    def parse_product(url: str) -> Product:
        pass