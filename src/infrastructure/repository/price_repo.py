from src.core.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.application.interfaces.repositories import PriceRepository
from src.infrastructure.database.mappers import PriceMapper
from src.domain.entities import Price
from src.infrastructure.database.models import ORMPrice


class PriceRepository:
    def __init__(self, session: AsyncSession):
        '''Инициализация репозитория с асинхронной сессией SQLAlchemy.'''
        self.session = session

    async def save(self, price: Price):
        try:
            # 1. Конвертация доменной сущности в ORM-объект
            orm_price = PriceMapper.to_orm(price)

            # 2. Добавление в сессию
            self.session.add(orm_price)

            # 3. flush() — отправляем в БД, получаем ID
            saved_price = await self.session.flush()

            # 4. Обновляем ID в доменном объекте
            price.id = saved_price.id

            return price
        except:
            pass

    async def get_last_price_for_product(self, product_id):
        try:
            # 1. Получение записи из базы данных
            stmt = (
                select(ORMPrice)
                .where(ORMPrice.product_id == product_id)
                .order_by(ORMPrice.created_at.desc())
            )
            result = await self.session.execute(stmt)
            orm_result = result.scalars().first()
            # ЧТО ТАМ?)
            return orm_result
        
        
        except:
            pass