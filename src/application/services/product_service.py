from typing import List
from datetime import datetime

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp
from src.interfaces.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

        def create_product(
                self,
                id: str,
                name: str,
                rating: float,
                price_with_card: int,
                price_without_card: int,
                previous_price_without_card: int,
                price_default: int,
                discount_amount: float,
                link: str,
                url_image: str,
                category_product: List[str],
                timestamp: datetime,
        )