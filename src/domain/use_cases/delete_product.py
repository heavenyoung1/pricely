import logging
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository

logger = logging.getLogger(__name__)

# Здесь находится бизнес-логика, которая управляет несколькими сущностями

class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: str):
        self.product_repo.delete(product_id)