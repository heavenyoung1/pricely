import logging
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository

logger = logging.getLogger(__name__)


class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: str) -> None:
        self.product_repo.delete(product_id)
        logger.info(f'Удаление продукта {product_id} инициировано')