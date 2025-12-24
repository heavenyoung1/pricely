from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities import Product
import logging
from sqlalchemy import select, func
from typing import Optional, List
from sqlalchemy.orm import Session
from src.core.logger import logger
from src.application.interfaces.repositories import ProductRepository
from src.infrastructure.database.mappers import ProductMapper, PriceMapper
from src.domain.entities import Product
from src.infrastructure.database.models import ORMProduct, ORMPrice, ORMUserProducts

from src.core.exceptions import EntityNotFoundException

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

            logger.info(f'Товар {product.name} получен')
            return product
        
        except:
            pass

    async def get(self, product_id: int) -> Optional['Product']:
        try:
            # 1. Получение записи из базы данных
            stmt = select(ORMProduct).where(ORMProduct.id == product_id)
            result = await self.session.execute(stmt)
            orm_product = result.scalars().first() # что такое scalars

            if not orm_product:
                raise EntityNotFoundException(f'Товар с {product_id} не существует')
            
            product = ProductMapper.to_domain(orm_product)
            logger.info(f'Товар получен - ID {product.id}')
        except:
            pass

    # ЕБАТЬ, ПО МОЕМУ ХУЕТА КАКАЯ ТО)
    async def get_all_products_id_for_user(self, user_id: str):
        stmt = (
            select(ORMUserProducts)
            .where(ORMUserProducts.user_id == user_id)
            .order_by(ORMUserProducts.created_at.desc()) # ДОБАВИТЬ CREATED_AT
        )
        result = await self.session.execute(stmt)
        orm_products = result.scalars().all()
        
        products = orm_products
        logger.info(f'Получено {len(products)} для пользователя {user_id}')
        data = dict()
        # ПРОТЕСТИРОВАТЬ ВООБЩЕ КАК ЭТО ВЫГЛЯДИТ!!!!
        data[user_id] = products

    async def get_all_data_products_for_user(self, user_id: str):
        stmt = (
            select(ORMProduct)
            .join(ORMUserProducts, ORMUserProducts.product_id == ORMProduct.id)
            .where(ORMUserProducts.user_id == user_id)
            .order_by(ORMUserProducts.created_at.desc())
        )
        result = await self.session.execute(stmt)
        orm_products = result.scalars().all()

        products = [ProductMapper.to_domain(product) for product in orm_products]
        logger.info(f'Получено {len(products)} для пользователя {user_id}')