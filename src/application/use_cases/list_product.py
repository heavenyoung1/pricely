import logging
from src.domain.repositories import ProductRepository
from src.domain.entities import Product

logger = logging.getLogger(__name__)

class ListProductsUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self) -> List[Product]:
        # Требование к ProductRepository: реализовать list_all()
        products = self.product_repo.list_all()
        logger.info(f"Получен список продуктов: {len(products)} шт.")
        return products
