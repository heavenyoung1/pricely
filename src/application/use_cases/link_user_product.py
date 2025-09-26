from src.application.interfaces.repositories import UserProductsRepository
import logging

logger = logging.getLogger(__name__)

class LinkUserProductUseCase:
    def __init__(
            self,
            user_products_repo: UserProductsRepository,
            ):
        self.user_products_repo = user_products_repo

    def  execute(self, user_id: str, product_id: str):
        '''Создаёт связь между пользователем и продуктом.'''
        existing = self.user_products_repo.get_products_for_user(user_id)
        if product_id in [row.product_id row in existing]:
            logger.info(f'Продукт {product_id} уже связан с пользователем {user_id}')
            return
    
        self.user_products_repo.add_product_for_user(user_id, product_id)
        logger.info(f'Успешно связали пользователя {user_id} с продуктом {product_id}')