
from datetime import datetime
from pydantic import ValidationError, validate_call
from typing import List
import logging

from src.domain.entities.product import Product
from src.domain.entities.price import PriceStamp
from src.interfaces.repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)

class ProductService:
    """
    Creates a new product with validated data.

    Args:
        **kwargs: Fields for Product model (id: str, name: str, rating: float, etc.)

    Returns:
        Product: The created product instance.

    Raises:
        ValidationError: If the provided data does not match the Product model schema.
    """
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    @validate_call
    def create_product(self, **kwargs) -> Product:
        try:
            product = Product(**kwargs)
            self.repository.save(product)
            logger.info(f'Product created {product.id}')
            return product
        except ValidationError as validate_error:
            logger.error(f'Validation Error, {validate_error}')
            raise
