import logging

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product, Price

logger = logging.getLogger(__name__)


class GetProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: str):
        return self.product_repo.get(product_id)