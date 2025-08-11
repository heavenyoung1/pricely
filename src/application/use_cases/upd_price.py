import logging
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Price

logger = logging.getLogger(__name__)


class UpdatePriceUseCase:
    def __init__(self, product_repo: ProductRepository, price_repo: PriceRepository):
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, price: Price, product_id: str):
        self.price_repo.save(price)
        product = self.product_repo.get(product_id)
        if product_id:
            product.price_id = price.id
            self.product_repo.save(product)