import logging
from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError

logger = logging.getLogger(__name__)


class GetFullProductUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        user_repo: UserRepository
    ):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo

    def execute(self, product_id: str):
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning(f'Продукт {product_id} не найден')
            raise ProductNotFoundError(f'Продукт {product_id} не найден')

        latest_price = self.price_repo.get_latest_for_product(product_id)
        latest = {
            "with_card": latest_price.with_card if latest_price else None,
            "without_card": latest_price.without_card if latest_price else None,
            "previous_price_with_card": latest_price.previous_with_card  if latest_price else None,
            "previous_price_without_card": latest_price.previous_without_card if latest_price else None,
        }

        return {
            "id": product.id,
            "name": product.name,
            "link": product.link,
            "image_url": product.image_url,
            "rating": product.rating,
            "categories": product.categories,
            "latest_price": latest,
            "created_at": latest_price.created_at,
        }

