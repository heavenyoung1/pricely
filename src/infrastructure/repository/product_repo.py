from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities import Product
import logging
from sqlalchemy import select, func
from typing import Optional, List
from sqlalchemy.orm import Session

from src.application.interfaces.repositories import ProductRepository
from src.infrastructure.database.mappers import ProductMapper, PriceMapper
from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct, ORMPrice

class ProductRepository:
    def __init__(self, session: AsyncSession):
        '''Инициализация репозитория с асинхронной сессией SQLAlchemy.'''
        self.session = session

    async def save(self, product: Product) -> 'Product':
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_product = ProductMapper.to_orm(product)

            # 2. Добавление в сессию
            saved_product = await self.session.add(orm_product)   
        
            # 3. flush() — отправляем в БД, получаем ID и timestamps
            await self.session.flush()
            product.id = saved_product.created_at

        except:
            pass

    # async def read(self, id: int) -> Optional['Product']:
    #     try:
    #         # 1. Получение записи из базы данных
    #         stmt = select(Prod)
    #     except:
    #         pass