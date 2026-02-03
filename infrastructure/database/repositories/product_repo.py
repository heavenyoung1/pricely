from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from core.logger import logger
from domain.entities.product import Product
from infrastructure.database.mappers.product import ProductMapper
from infrastructure.database.models.product import ORMProduct

from domain.exceptions import (
    ProductNotFoundError,
    DatabaseError,
)


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, product: Product) -> 'Product':
        try:
            # 1. Конвертация Domain → ORM
            orm_product = ProductMapper.to_orm(product)

            # 2. Добавление в сессию
            self.session.add(orm_product)

            # 3. flush() — отправляем в БД, получаем ID
            await self.session.flush()

            # 4. Конвертируем обратно ORM → Domain (с ID)
            product.id = orm_product.id

            # Возвращаем доменную сущность
            logger.info(f'Товар с ID {product.id} успешно сохранен в БД.')
            return product

        except SQLAlchemyError as error:
            message = f'Ошибка при сохранении товара: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get(self, id: int) -> Optional['Product']:
        try:
            # 1. Формируем запрос
            statement = select(ORMProduct).where(ORMProduct.id == id)
            result = await self.session.execute(statement)
            orm_product = result.scalar_one_or_none()

            # 2. Проверка существования записи в БД
            if not orm_product:
                logger.error(f'Товар с ID = {id} не найден')
                return None

            # 3. Конвертируем ORM → Domain
            product = ProductMapper.to_domain(orm_product)
            return product

        except SQLAlchemyError as error:
            message = f'Ошибка при получении товара: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get_many(self, ids: List[int]) -> List[Product]:
        try:
            if not ids:
                return []

            statement = select(ORMProduct).where(ORMProduct.id.in_(ids))
            result = await self.session.execute(statement)
            orm_products = result.scalars().all()

            return [ProductMapper.to_domain(p) for p in orm_products]

        except SQLAlchemyError as error:
            message = f'Ошибка при получении товаров: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get_link(self, id: int) -> Optional['Product']:
        try:
            # 1. Формируем запрос
            statement = select(ORMProduct).where(ORMProduct.id == id)
            result = await self.session.execute(statement)
            orm_product = result.scalar_one_or_none()

            # 2. Проверка существования записи в БД
            if not orm_product:
                logger.error(f'Товар с ID = {id} не найден')
                return None

            # 3. Конвертируем ORM → Domain
            product = ProductMapper.to_domain(orm_product)
            link = product.link
            return link

        except SQLAlchemyError as error:
            message = f'Ошибка при получении товара: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def update(self, product: Product) -> 'Product':
        try:
            # 1. Проверка наличия ID
            if product.id is None:
                raise ValueError(f'Передан товар без ID')

            # 2. Получаем существующий ORM объект
            statement = select(ORMProduct).where(ORMProduct.id == product.id)
            result = await self.session.execute(statement)
            orm_product = result.scalar_one_or_none()

            # 3. Проверка существования
            if orm_product is None:
                raise ProductNotFoundError(product.id)

            # 4. Обновляем ORM объект из Domain
            updated_orm = ProductMapper.to_orm(product)
            # Обновляем атрибуты существующего объекта
            orm_product.article = updated_orm.article
            orm_product.name = updated_orm.name
            orm_product.link = updated_orm.link

            # 5. flush() — применяем изменения
            await self.session.flush()

            # 6. Возвращаем обновленную Domain сущность
            updated_product = ProductMapper.to_domain(orm_product)
            logger.info(f'Товар обновлен: ID = {updated_product.id}')
            return updated_product
        except ProductNotFoundError:
            raise  # Пробрасываем доменное исключение дальше
        except SQLAlchemyError as error:
            message = f'Ошибка при обновлении товара: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def get_by_link(self, link: str) -> Optional['Product']:
        try:
            statement = select(ORMProduct).where(ORMProduct.link == link)
            result = await self.session.execute(statement)
            orm_product = result.scalar_one_or_none()

            if not orm_product:
                return None

            product = ProductMapper.to_domain(orm_product)
            return product

        except SQLAlchemyError as error:
            message = f'Ошибка при поиске товара по ссылке: {error}'
            logger.error(message)
            raise DatabaseError(message)

    async def delete(self, id: int) -> bool:
        try:
            # 1. Получаем ORM объект
            statement = select(ORMProduct).where(ORMProduct.id == id)
            result = await self.session.execute(statement)
            orm_product = result.scalar_one_or_none()

            # 2. Если не найден
            if not orm_product:
                logger.error(f'Товар с ID = {id} не найден')
                return False

            # 3. Удаляем
            self.session.delete(orm_product)
            await self.session.flush()

            logger.info(f'Товар с ID {id} удален')
            return True
        except SQLAlchemyError as error:
            message = f'Ошибка при удалении товара: {error}'
            logger.error(message)
            raise DatabaseError(message)
