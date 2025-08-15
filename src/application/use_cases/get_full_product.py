import logging
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product

logger = logging.getLogger(__name__)

class GetFullProductUseCase:
    def __init__(
        self, 
        product_repo: ProductRepository, 
        price_repo: UserRepository, 
        user_repo: UserRepository
        ):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo

    def execute(self, product_id: str):
        product = self.product_repo.get(product_id)
        if not product:
            return None
        
        if product.price_id:
            price = self.price_repo.get(product.price_id)

        user = self.user_repo.get(product.user_id)
        return {
            'product': product,
            'price': price,
            'user': user,
        }

