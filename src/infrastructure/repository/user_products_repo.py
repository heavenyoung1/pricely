import logging
from typing import TYPE_CHECKING, Optional

from src.core.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.application.interfaces.repositories import UserProductsRepository
from src.infrastructure.database.mappers import UserMapper
from src.infrastructure.database.models import ORMUserProducts

from src.application.interfaces.repositories import UserRepository
from src.infrastructure.database.mappers import UserMapper
from src.infrastructure.database.models import ORMUser

from sqlalchemy.orm import Session

class UserProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, user_product: tuple):
        # 1. Конвертация доменной сущности в ORM-объект
        self.session.add(user_product)

        await self.session.flush()

        return True
    
    async def get

