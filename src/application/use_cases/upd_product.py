import logging
from src.domain.repositories import ProductRepository, PriceRepository
from src.domain.entities import Product, Price

logger = logging.getLogger(__name__)


class ProductNotFoundError(Exception):
    '''Исключение для случаев, когда продукт не найден.'''
    pass

class PriceUpdateError(Exception):
    '''Исключение для ошибок при обновлении цены.'''
    pass

class UpdateProductPriceUseCase:
    def __init__(self, product_repo: ProductRepository, price_repo: PriceRepository):
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, product_id: str, price: Price) -> None:
        try:
            # Валидация входных данных
            if not product_id:
                logger.error('Идентификатор продукта не указан')
                raise PriceUpdateError('Идентификатор продукта не указан')
            if not price.id:
                logger.error('Идентификатор цены не указан')
                raise PriceUpdateError('Идентификатор цены не указан')


            product = self.product_repo.get(product_id)
            if not product:
                logger.warning(f'Продукт с id {product_id} не найден')
                raise ProductNotFoundError(f'Продукт с id {product_id} не найден')

            # 1) сохраняем новую цену
            self.price_repo.save(price)
            logger.debug(f'Цена {price.id} сохранена для продукта {product_id}')

            # 2) обновляем price_id в продукте
            product.price_id = price.id
            self.product_repo.save(product)
            logger.debug(f'Продукт {product_id} обновлен с price_id={price.id}')

            logger.info(f'Цена успешно обновлена для продукта {product_id}, price_id={price.id}')
        except Exception as e:
            logger.error(f'Ошибка при обновлении цены для продукта {product_id}: {str(e)}')
            raise PriceUpdateError(f'Ошибка при обновлении цены: {str(e)}')
