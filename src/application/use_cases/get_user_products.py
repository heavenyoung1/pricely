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
    '''Извлекает все записи user_id и product_id.'''
    def __init__(
        self,
        user_products_repo: UserProductsRepository,
    ):
        self.user_products_repo = user_products_repo

    def execute(self) -> dict:
        logger.info(f'Запрашиваем данные для запуска  APSchedulerService')
        return self.user_products_repo.get_all_user_products_pair()
            