
from datetime import datetime
from pydantic import ValidationError, validate_call
from typing import List
import logging

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp
from src.interfaces.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    @validate_call
    def create_product(self, **kwargs) -> Product:
        try:
            product = Product(**kwargs)
            self.repository.save(product)
            return product
        except ValidationError as validate_error:
            logger.error(f'Error of Validate Error, {validate_error}')

        # def create_product(
        #         self,
        #         id: str,
        #         name: str,
        #         rating: float,
        #         price_with_card: int,
        #         price_without_card: int,
        #         previous_price_without_card: int,
        #         price_default: int,
        #         discount_amount: float,
        #         link: str,
        #         url_image: str,
        #         category_product: List[str],
        #         timestamp: datetime,
        # ) -> Product:
        #     product = Product(
        #         id=id,
        #         name=name,
        #         rating=rating,
        #         price_with_card=price_with_card,
        #         price_without_card=price_without_card,
        #         previous_price_without_card=previous_price_without_card,
        #         price_default=price_default,
        #         discount_amount=discount_amount,
        #         link=link,
        #         url_image=url_image,
        #         category_product=category_product,
        #         timestamp=timestamp,
        #     )
        #     self.repository.save(product)
        #     return product
