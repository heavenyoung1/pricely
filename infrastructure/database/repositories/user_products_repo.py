from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict

from core.logger import logger
from domain.entities.user_products import UserProducts
from infrastructure.database.mappers.user_products import UserProductsMapper
from infrastructure.database.models.user_products import ORMUserProducts

from domain.exceptions import DatabaseError


class UserProductsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user_id: int, product_id: int) -> 'UserProducts':
        try:
            # 1. Создаем domain entity
            user_products = UserProducts(user_id=user_id, product_id=product_id)

            # 2. Конвертация Domain → ORM
            orm_user_products = UserProductsMapper.to_orm(user_products)

            # 3. Добавление в сессию
            self.session.add(orm_user_products)

            # 4. flush() — отправляем в БД
            await self.session.flush()

            # Возвращаем доменную сущность
            logger.info(
                f'Связь пользователь-товар сохранена: user_id={user_id}, product_id={product_id}'
            )
            return user_products

        except SQLAlchemyError as error:
            message = f'Ошибка при сохранении связи пользователь-товар: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get_all_by_user(self, user_id: int) -> List[int]:
        '''Получить все товары пользователя (список ID товаров)'''
        try:
            # 1. Формируем запрос
            statement = select(ORMUserProducts).where(
                ORMUserProducts.user_id == user_id
            )
            result = await self.session.execute(statement)
            orm_user_products = result.scalars().all()

            # 2. Конвертируем ORM → Domain и извлекаем product_id
            product_ids = [orm.product_id for orm in orm_user_products]
            logger.info(
                f'Найдено {len(product_ids)} товаров для пользователя с ID = {user_id}'
            )
            return product_ids

        except SQLAlchemyError as error:
            message = f'Ошибка при получении товаров пользователя: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def delete(self, user_id: int, product_id: int) -> bool:
        '''Удалить связь пользователь-товар'''
        try:
            # 1. Получаем ORM объект
            statement = select(ORMUserProducts).where(
                ORMUserProducts.user_id == user_id,
                ORMUserProducts.product_id == product_id,
            )
            result = await self.session.execute(statement)
            orm_user_products = result.scalar_one_or_none()

            # 2. Если не найден
            if not orm_user_products:
                logger.warning(
                    f'Связь пользователь-товар не найдена: user_id={user_id}, product_id={product_id}'
                )
                return False

            # 3. Удаляем
            self.session.delete(orm_user_products)
            await self.session.flush()

            logger.info(
                f'Связь пользователь-товар удалена: user_id={user_id}, product_id={product_id}'
            )
            return True

        except SQLAlchemyError as error:
            message = f'Ошибка при удалении связи пользователь-товар: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get_all_grouped(self) -> Dict[int, List[int]]:
        '''Получить сгруппированные данные: словарь {user_id: [product_ids]}'''
        try:
            # 1. Получаем все записи
            statement = select(ORMUserProducts)
            result = await self.session.execute(statement)
            orm_user_products = result.scalars().all()

            # 2. Группируем по user_id
            grouped: Dict[int, List[int]] = {}
            for orm in orm_user_products:
                user_id = orm.user_id
                product_id = orm.product_id

                if user_id not in grouped:
                    grouped[user_id] = []
                grouped[user_id].append(product_id)

            logger.info(f'Найдено {len(grouped)} пользователей с товарами')
            return grouped

        except SQLAlchemyError as error:
            message = f'Ошибка при получении сгруппированных данных: {error}'
            logger.error(message)
            raise DatabaseError(message)
