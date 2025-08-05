from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.product import Product
from domain.entities.price_claim import PriceStamp

class PriceRepository(ABC):
    @abstractmethod
    def save_price_stamp(self, product: Product, price_stamp: PriceStamp):
        pass

    @abstractmethod
    def delete_stamps_for_product(self, product: Product, price_stamp: PriceStamp):
        pass