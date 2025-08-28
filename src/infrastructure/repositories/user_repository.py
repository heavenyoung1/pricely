import logging

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUser

from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

class UserRepositoryImpl(UserRepository):
    '''Реализация репозитория для работы с пользователями в базе данных.'''
    def __init__(self, session: Session):
        self.session = session

    def save(self, user):
        self.session.merge(UserMapper.domain_to_orm(user))

    def get(self, user_id):
        orm_user = self.session.get(ORMUser, user_id)
        if orm_user:
            user = UserMapper.orm_to_domain(orm_user)
            logger.info(f"Пользователь {user} получен по id: {user_id}")
            return user
        logger.warning(f"Пользователь с id {user_id} не найден")
        return None
    
    def delete(self, user_id: str) -> None:
        logger.info(f"Попытка удаления пользователя с ID: {user_id}")
        try:
            orm_user = self.session.get(ORMUser, user_id)
            if not orm_user:
                logger.warning(f"Пользователь с id {user_id} не найден")
                return
            self.session.delete(orm_user)
            logger.info(f"Пользователь с id: {user_id} удален")
        except Exception as e:
            logger.error(f"Ошибка удаления пользователя {user_id}: {str(e)}")
            raise