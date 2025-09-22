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
        '''
        Возвращает список product_id, связанных с пользователем.
        '''
        logger.debug(f"Получение списка продуктов для пользователя {user_id}")
        rows = (
        self.session.query(ORMUserProducts).filter(ORMUserProducts.user_id == user_id).all()
        )
        logger.debug([row for row in rows])
        return [row for row in rows]