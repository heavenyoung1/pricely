import logging
from typing import TYPE_CHECKING, Optional
from src.domain.entities import User
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


from src.application.interfaces.repositories import UserRepository
from src.infrastructure.database.mappers import UserMapper
from src.infrastructure.database.models import ORMUser

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User):
        # 1. Конвертация доменной сущности в ORM-объект
        orm_user = UserMapper.to_orm(user)

        # 2. Добавление в сессию
        self.session.add(orm_user)

        # 3. flush() — отправляем в БД, получаем ID
        await self.session.flush()

        return user
    
    async def get(self, user_id: int) -> Optional['User']:
        # 1. Получение записи из базы данных
        stmt = select(ORMUser).where(ORMUser.id == user_id)
        result = await self.session.execute(stmt)
        orm_user = result.scalars().first()

        if not orm_user:
            return None
        
        user = UserMapper.to_domain(orm_user)
        return user