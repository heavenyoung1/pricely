import logging
from typing import TYPE_CHECKING, Optional

from src.application.interfaces.repositories import UserRepository
from src.infrastructure.database.mappers import UserMapper
from src.infrastructure.database.models import ORMUser

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.domain.entities import User

class UserRepositoryImpl(UserRepository):
    '''Реализация репозитория для работы с пользователями в базе данных.'''

    def __init__(self, session: Session):
        '''
        Инициализация репозитория для работы с пользователями.

        :param session: Экземпляр SQLAlchemy Session для работы с базой данных.
        '''
        self.session = session

    def save(self, user) -> None:
        '''
        Сохранить или обновить пользователя в базе данных.

        :param user: Объект типа User, который необходимо сохранить или обновить.
        '''
        try:
            # Преобразуем доменную модель пользователя в ORM модель и сохраняем
            self.session.merge(UserMapper.domain_to_orm(user))
            logger.info(f'Пользователь {user.id} успешно сохранен/обновлен')
        except Exception as e:
            logger.error(f'Ошибка сохранения пользователя {user}: {str(e)}')
            raise

    def get(self, user_id: str) -> Optional['User']:
        '''
        Получить пользователя по идентификатору.

        :param user_id: Идентификатор пользователя.
        :return: Объект User, если найден, иначе None.
        '''
        try:
            orm_user = self.session.get(ORMUser, user_id)
            if orm_user:
                user = UserMapper.orm_to_domain(orm_user)
                logger.info(f'Пользователь {user} получен по id: {user_id}')
                return user
            logger.warning(f'Пользователь с id {user_id} не найден')
            return None
        except Exception as e:
            logger.error(f'Ошибка получения пользователя с id {user_id}: {str(e)}')
            raise

    def delete(self, user_id: str) -> None:
        '''
        Удалить пользователя по идентификатору.

        :param user_id: Идентификатор пользователя, которого нужно удалить.
        :raises Exception: Если произошла ошибка при удалении пользователя.
        '''
        logger.info(f'Попытка удаления пользователя с ID: {user_id}')
        try:
            orm_user = self.session.get(ORMUser, user_id)
            if not orm_user:
                logger.warning(f'Пользователь с id {user_id} не найден')
                return
            self.session.delete(orm_user)
            logger.info(f'Пользователь с id {user_id} успешно удален')
        except Exception as e:
            logger.error(f'Ошибка удаления пользователя с id {user_id}: {str(e)}')
            raise