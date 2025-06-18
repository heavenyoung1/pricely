from adapters.interfaces import IMarketPlace
from models.product import Product

class PriceParser():
    def __init__(self, adapters: dict[str, IMarketPlace]):
        self.adapters = adapters

    def parse(self, url: str, marketplace: str) -> Product:
        adapter = self.adapters.get(marketplace)
        if adapter is None:
            raise ValueError(f'Маркетплейс {marketplace} не поддерживается')
        return adapter.parse_product(url)