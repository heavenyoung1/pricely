import logging
from src.domain.repositories import ProductRepository

logger = logging.getLogger(__name__)

class ListProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self):
        logger.info("Получен список всех продуктов")
        return list(self.product_repo.products.values())
