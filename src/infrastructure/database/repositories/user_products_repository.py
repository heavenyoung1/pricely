import logging

from src.application.interfaces.repositories import UserProductsRepository
from src.infrastructure.database.mappers import UserMapper
from src.infrastructure.database.models import ORMUserProducts

from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

class UserProductsRepositoryImpl(UserProductsRepository):
    '''Реализация репозитория для работы с товарами пользователя в базе данных.'''
    def __init__(self, session: Session):
        self.session = session

    def get_products_for_user(self, user_id):
        logger.debug(f"Получение списка продуктов для пользователя {user_id}")
        rows = (
            self.session.query(ORMUserProducts)
            .filter(ORMUserProducts.user_id == user_id)
            .all()
        )
        logger.debug(f'ПРОДУКТЫ ПОЛЬЗОВАТЕЛЯ В СПИСКЕ!!! - {[row.product_id for row in rows]}')
        logger.debug(f"Продукты пользователя {user_id}: {[row.product_id for row in rows]}")
        return [row.product_id for row in rows]
    
    def add_product_for_user(self, user_id: str, product_id: str) -> None:
        '''Создаёт запись в user_products (связка user_id и product_id).'''
        logger.info(f'Привязка товара ID {product_id} пользователю ID {user_id}')
        reccord = ORMUserProducts(user_id=user_id, product_id=product_id)
        self.session.add(reccord)

    def get_all_user_products_pair(self) -> None:
        logger.info('Извлекаем данные {product_id:user_id} из репозитория UserProductsRepositoryImpl')
        rows = (
            self.session.query(ORMUserProducts).all()
        )
        records = [{'product_id': row.product_id, 'user_id': row.user_id} for row in rows]
        logger.info(f'Записи список(словарей) получен и готов для парсинга.')
        return logger