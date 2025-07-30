from datetime import datetime
from pydantic import ValidationError, validate_call
from typing import List, Optional
import logging

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp
from src.interfaces.repositories.price_repository import PriceRepository

logger = logging.getLogger(__name__)

class PriceStampService:
    def __init__(self, repository: PriceRepository):
        self.repository = repository

    def create_price_stamp(self, **kwargs) -> PriceStamp:
        try:
            price_stamp = PriceStamp(**kwargs)
            self.repository.save_price_stamp(price_stamp)
            logger.info(f'Price with ID: {price_stamp.ID_product} claimed, time:{price_stamp.time_stamp}!')
            return price_stamp
        except Exception as e:
            logger.error(f'Error of price claim, {e}')
            raise 






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