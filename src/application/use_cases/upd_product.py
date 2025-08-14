import logging
from src.domain.repositories import ProductRepository
from src.domain.entities import Product

logger = logging.getLogger(__name__)

class UpdateProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product: Product):
        product = self.product_repo.get(product_id)
        if product:
            product.price_id = price.id
            self.product_repo.save(product)
        else:
            raise ValueError(f"Продукт с id {product_id} не найден")
