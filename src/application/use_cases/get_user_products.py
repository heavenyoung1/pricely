from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserRepository, UserProductsRepository
from src.domain.entities import Product, Price, User

from src.infrastructure.parsers import OzonParser
from datetime import datetime
import logging
import uuid
from src.infrastructure.parsers.interfaces import Parser
from src.application.interfaces import ProductParser
from src.domain.exceptions import ParserProductError, ProductCreationError
from typing import List

logger = logging.getLogger(__name__)

class GetUserProductsUseCase:
    def __init__(
        self,
        user_products_repo: UserProductsRepository,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
    ):
        self.user_products_repo = user_products_repo
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, user_id: str) -> List[str]:
        logger.info(f'Запрос списка товар для пользователя ID: {user_id}')
        
        product_ids = self.user_products_repo.get_products_for_user(user_id)
        if not product_ids:
            return []
        
        products = []
        for product_id in product_ids:
            product = self.product_repo.get(product_id=product_id)
            if not product:
                continue

            latest_price = self.price_repo.get_latest_for_product(product_id)

            products.append({
                "id": product.id,
                "name": product.name,
                "link": product.link,
                "image_url": product.image_url,
                "rating": product.rating,
                "categories": product.categories,
                "latest_price": {
                    "with_card": latest_price.with_card if latest_price else None,
                    "without_card": latest_price.without_card if latest_price else None,
                    #"default_price": latest_price.default_price if latest_price else None,
                }
            })

        return products

    