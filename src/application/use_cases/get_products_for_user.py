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

class GetProductForUserUseCase:
    def __init__(
        self,
        user_products_repo: UserProductsRepository,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
    ):
        self.user_products_repo = user_products_repo
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, user_id: str) -> list:
        logger.info(f"Запрос списка товаров для пользователя ID: {user_id}")
        raw_ids = self.user_products_repo.get_products_for_user(user_id)
        if not raw_ids:
            return []
        ids = [str(x) for x in raw_ids]
        logger.debug(f"User {user_id} product ids: {ids}")
        return ids

    