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

        # Все цены этого продукта
        prices = self.price_repo.get_all_prices_by_product(product_id)
        # Пользователь
        user = self.user_repo.get(product.user_id)

        return {
            'id': product.id,
            'name': product.name,
            'link': product.link,
            'image_url': product.image_url,
            'rating': product.rating,
            'categories': product.categories,
            'prices': [vars(p) for p in prices],
            'user': vars(user) if user else None,
        }

