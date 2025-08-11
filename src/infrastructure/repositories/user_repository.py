import logging

from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.infrastructure.mappers import ProductMapper, PriceMapper, UserMapper
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUser
from src.infrastructure.database.core import with_session

from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)

class UserRepositoryImpl(UserRepository):
    '''Реализация репозитория для работы с пользователями в базе данных.'''
    @with_session
    def save(self, user, session: Session):
        '''
        Сохраняет или обновляет пользователя в БД.
        
        Args:
            user (User): Доменный объект пользователя
            session (Session): Сессия SQLAlchemy
            
        Raises:
            DatabaseError: При ошибках работы с БД
        '''
        self.session.merge(UserMapper.to_orm(user))

    @with_session
    def get(self, user_id, session: Session):
        '''
        Получает пользователя по ID из БД.
        
        Args:
            user_id (str): Идентификатор пользователя
            session (Session): Сессия SQLAlchemy
            
        Returns:
            Optional[User]: Найденный пользователь или None
        '''
        orm_user = session.get(ORMUser, user_id)
        if orm_user:
            user = UserMapper.to_domain(orm_user)
            logger.info(f"Пользователь {user} получен по id: {user_id}")
            return user
        logger.warning(f"Пользователь с id {user_id} не найден")
        return None
    
    @with_session
    def delete(self, user_id: str, session: Session) -> None:
        '''
        Удаляет пользователя по ID из БД.
        
        Args:
            user_id (str): Идентификатор пользователя
            session (Session): Сессия SQLAlchemy
            
        Raises:
            DatabaseError: При ошибках удаления
        '''
        orm_user = self.session(ORMUser, user_id)
        if orm_user:
            session.delete(ORMUser, orm_user)
            logger.info(f"Пользователь c id: {user_id} удален")
        logger.warning(f"Пользователь с id {user_id} не найден")
        return None