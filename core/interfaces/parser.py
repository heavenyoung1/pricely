from abc import ABC, abstractmethod

from core.models.product import Product

class IProductParser(ABC):
    @abstractmethod
    async def parse(self, url: str) -> 'Product':
        pass

    @abstractmethod
    def get_marketplace(self) -> str:
        pass

class IProductParserFactory(ABC):
    @abstractmethod
    def get_parser(self, url: str) -> IProductParser:
        pass