from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp

class PriceRepository(ABC):
    @abstractmethod
    def save_price_stamp(self, product: Product, price_stamp: PriceStamp)
        pass

    @abstractmethod
    def delete_all_stamps(self, product: Product, price_stamp: PriceStamp)
        pass