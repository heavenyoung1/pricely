from sqlalchemy import select, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from src.core.logger import logger
from src.domain.entities.price import Price
from src.infrastructure.database.mappers.price import PriceMapper
from src.infrastructure.database.models.price import ORMPrice

from src.domain.exceptions import DatabaseError


class PriceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, price: Price) -> 'Price':
        try:
            # 1. Конвертация Domain → ORM
            orm_price = PriceMapper.to_orm(price)

            # 2. Добавление в сессию
            self.session.add(orm_price)

            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Конвертируем обратно ORM → Domain (с ID)
            price.id = orm_price.id

            # Возвращаем доменную сущность
            logger.info(f'Цена с ID {price.id} успешно сохранена в БД.')
            return price

        except SQLAlchemyError as error:
            message = f'Ошибка при сохранении цены: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get_actual(self, product_id: int) -> Optional['Price']:
        try:
            # 1. Формируем запрос: последняя цена по created_at
            statement = (
                select(ORMPrice)
                .where(ORMPrice.product_id == product_id)
                .order_by(desc(ORMPrice.created_at))
                .limit(1)
            )
            result = await self.session.execute(statement)
            orm_price = result.scalar_one_or_none()

            # 2. Проверка существования записи в БД
            if not orm_price:
                logger.warning(
                    f'Актуальная цена для товара с ID = {product_id} не найдена'
                )
                return None

            # 3. Конвертируем ORM → Domain
            price = PriceMapper.to_domain(orm_price)
            return price

        except SQLAlchemyError as error:
            message = f'Ошибка при получении актуальной цены: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get_all_by_product(self, product_id: int) -> List['Price']:
        try:
            # 1. Формируем запрос: все цены товара, отсортированные по дате
            statement = (
                select(ORMPrice)
                .where(ORMPrice.product_id == product_id)
                .order_by(desc(ORMPrice.created_at))
            )
            result = await self.session.execute(statement)
            orm_prices = result.scalars().all()

            # 2. Конвертируем ORM → Domain
            prices = [PriceMapper.to_domain(orm_price) for orm_price in orm_prices]
            logger.info(f'Найдено {len(prices)} цен для товара с ID = {product_id}')
            return prices

        except SQLAlchemyError as error:
            message = f'Ошибка при получении всех цен товара: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def delete_by_product(self, product_id: int) -> int:
        '''Удалить все цены для товара. Возвращает количество удаленных записей'''
        try:
            # 1. Получаем все ORM объекты для удаления
            statement = select(ORMPrice).where(ORMPrice.product_id == product_id)
            result = await self.session.execute(statement)
            orm_prices = result.scalars().all()

            # 2. Если не найдено
            if not orm_prices:
                logger.warning(f'Цены для товара с ID = {product_id} не найдены')
                return 0

            # 3. Удаляем все найденные записи
            count = len(orm_prices)
            for orm_price in orm_prices:
                self.session.delete(orm_price)
            await self.session.flush()

            logger.info(f'Удалено {count} цен для товара с ID {product_id}')
            return count

        except SQLAlchemyError as error:
            message = f'Ошибка при удалении цен товара: {error}'
            logger.error(message)
            raise DatabaseError(message)
