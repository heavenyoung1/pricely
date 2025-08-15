import logging
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product

logger = logging.getLogger(__name__)

class GetFullProductUseCase:
    def __init__(self, product_repo: ProductRepository, price_repo: UserRepository, user_repo: UserRepository):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo

    def execute(self):
        
