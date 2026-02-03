from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from core.logger import logger
from domain.entities.user import User
from infrastructure.database.mappers.user import UserMapper
from infrastructure.database.models.user import ORMUser

from domain.exceptions import (
    UserNotFoundError,
    DatabaseError,
)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> 'User':
        try:
            # 1. Конвертация Domain → ORM
            orm_user = UserMapper.to_orm(user)

            # 2. Добавление в сессию
            self.session.add(orm_user)

            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Конвертируем обратно ORM → Domain (с ID)
            user.id = orm_user.id

            # Возвращаем доменную сущность
            logger.info(f'Пользователь с ID {user.id} успешно сохранен в БД.')
            return user

        except SQLAlchemyError as error:
            message = f'Ошибка при сохранении пользователя: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get(self, id: int) -> Optional['User']:
        try:
            # 1. Формируем запрос
            statement = select(ORMUser).where(ORMUser.id == id)
            result = await self.session.execute(statement)
            orm_user = result.scalar_one_or_none()

            # 2. Проверка существования записи в БД
            if not orm_user:
                logger.error(f'Пользователь с ID = {id} не найден')
                return None

            # 3. Конвертируем ORM → Domain
            user = UserMapper.to_domain(orm_user)
            return user
        except SQLAlchemyError as error:
            message = f'Ошибка при получении пользователя: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get_by_chat_id(self, chat_id: str) -> Optional['User']:
        try:
            statement = select(ORMUser).where(ORMUser.chat_id == chat_id)
            result = await self.session.execute(statement)
            orm_user = result.scalar_one_or_none()

            if not orm_user:
                return None

            return UserMapper.to_domain(orm_user)
        except SQLAlchemyError as error:
            message = f'Ошибка при получении пользователя по chat_id: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def update(self, user: User) -> 'User':
        try:
            # 1. Проверка наличия ID
            if user.id is None:
                raise ValueError(f'Передан пользователь без ID')

            # 2. Получаем существующий ORM объект
            statement = select(ORMUser).where(ORMUser.id == user.id)
            result = await self.session.execute(statement)
            orm_user = result.scalar_one_or_none()

            # 3. Проверка существования
            if orm_user is None:
                raise UserNotFoundError(user.id)

            # 4. Обновляем ORM объект из Domain
            updated_orm = UserMapper.to_orm(user)
            # Обновляем атрибуты существующего объекта
            orm_user.name = updated_orm.name
            orm_user.chat_id = updated_orm.chat_id

            # 5. flush() — применяем изменения
            await self.session.flush()

            # 6. Возвращаем обновленную Domain сущность
            updated_user = UserMapper.to_domain(orm_user)
            logger.info(f'Пользователь обновлен: ID = {updated_user.id}')
            return updated_user
        except UserNotFoundError:
            raise  # Пробрасываем доменное исключение дальше
        except SQLAlchemyError as error:
            message = f'Ошибка при обновлении пользователя: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def delete(self, id: int) -> bool:
        try:
            # 1. Получаем ORM объект
            statement = select(ORMUser).where(ORMUser.id == id)
            result = await self.session.execute(statement)
            orm_user = result.scalar_one_or_none()

            # 2. Если не найден
            if not orm_user:
                logger.error(f'Пользователь с ID = {id} не найден')
                return False

            # 3. Удаляем
            self.session.delete(orm_user)
            await self.session.flush()

            logger.info(f'Пользователь с ID {id} удален')
            return True
        except SQLAlchemyError as error:
            message = f'Ошибка при удалении пользователя: {error}'
            logger.error(message)
            raise DatabaseError(message)
