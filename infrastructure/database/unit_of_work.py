from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from infrastructure.database.repositories.product_repo import ProductRepository
from infrastructure.database.repositories.price_repo import PriceRepository
from infrastructure.database.repositories.user_repo import UserRepository
from infrastructure.database.repositories.user_products_repo import (
    UserProductsRepository,
)
from infrastructure.database.repositories.general_repo import (
    GeneralRepository,
)
from core.config.database import DataBaseConnection
from core.logger import logger


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        # Инициализация репозиториев с общей сессией
        self.user_repo = UserRepository(session)
        self.product_repo = ProductRepository(session)
        self.price_repo = PriceRepository(session)
        self.user_products_repo = UserProductsRepository(session)
        self.general_repo = GeneralRepository(session)

    async def __aenter__(self):
        '''Вход в async context manager.'''
        logger.debug('UnitOfWork инициализирован')
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        '''Выход из async context manager.'''
        try:
            if exc_type is not None:
                # ❌ Была ошибка - откатываем
                logger.warning(f'Исключение в UoW: {exc_type.__name__}: {exc_val}')
                await self.rollback()
            else:
                # ✅ Всё ОК - коммитим
                await self.commit()
        finally:
            # Не закрываем сессию! Database отвечает за это
            logger.info('AsyncUnitOfWork завершил работу')

    async def commit(self) -> None:
        '''Фиксация изменений.'''
        if self.session:
            try:
                await self.session.commit()
                logger.info('Транзакция зафиксирована')
            except Exception as e:
                logger.error(f'❌ Ошибка при коммите: {e}')
                raise

    async def rollback(self) -> None:
        '''Откат изменений.'''
        if self.session:
            try:
                await self.session.rollback()
                logger.info('Транзакция откачена')
            except Exception as e:
                logger.error(f'КРИТИЧЕСКАЯ ОШИБКА при rollback: {e}')
                raise


class UnitOfWorkFactory:
    def __init__(self, db: DataBaseConnection):
        self.db = db
        logger.debug('UnitOfWorkFactory инициализирована')

    @asynccontextmanager
    async def create(self) -> AsyncGenerator[UnitOfWork, None]:
        '''
        Создаёт UnitOfWork с управлением сессией.

        Использование:
            async with factory.create() as uow:
                await uow.attorney_repo.get(1)
        '''
        async with self.db.get_session() as session:
            uow = UnitOfWork(session)
            async with uow:
                yield uow

    async def close(self) -> None:
        '''Закрытие соединений с БД при завершении приложения.'''
        await self.db.dispose()
        logger.info('DataBaseConnection закрыта')
