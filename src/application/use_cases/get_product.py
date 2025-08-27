import logging
from typing import Optional

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product, Price
from exceptions import ProductNotFoundError

logger = logging.getLogger(__name__)


class GetProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    def execute(self, product_id: str) -> Product: 
        try:
            if not product_id:
                logger.error('Идентификатор продукта не указан')
                raise ProductNotFoundError('Идентификатор продукта не указан')

            product = self.product_repo.get(product_id)
            if not product:
                logger.warning(f'Продукт {product_id} не найден')
                raise ProductNotFoundError(f'Продукт {product_id} не существует')

            logger.info(f'Продукт {product_id} успешно получен')
            return product

        except ProductNotFoundError:
            raise
        except Exception as e:
            logger.error(f'Ошибка при получении продукта {product_id}: {str(e)}')
            raise ProductNotFoundError(f'Ошибка при получении продукта: {str(e)}')