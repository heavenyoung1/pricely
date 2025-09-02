from abc import ABC, abstractmethod

class ProductParser(ABC):
    @abstractmethod
    def parse_product(self, url: str) -> dict:
        pass