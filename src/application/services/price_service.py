from datetime import datetime
from pydantic import ValidationError, validate_call
from typing import List, Optional
import logging

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp
from src.interfaces.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class PriceStampService:
    def create_price_stamp(self, **kwargs) -> PriceStamp:
        price_stamp = PriceStamp(**kwargs)
        





    @validate_call
    def create_product(self, **kwargs) -> Product:
        try:
            product = Product(**kwargs)
            self.repository.save(product)
            logger.info(f'Product with ID: {product.id} has been created!')
            return product
        except ValidationError as validate_error:
            logger.error(f'Validation Error, {validate_error}')
            raise