import logging
from src.domain.repositories import ProductRepository
from src.domain.entities import Product

logger = logging.getLogger(__name__)

class UpdateProductInfoUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product: Product):
        existing = self.product_repo.get(product.id)
        if not existing:
            raise ValueError("Продукт не найден")
        self.product_repo.save(product)
        logger.info(f"Информация о продукте {product.id} обновлена")
