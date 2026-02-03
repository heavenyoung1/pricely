import asyncio

from core.config.database import DataBaseConnection
from core.logger import logger
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from infrastructure.parsers.browser import BrowserManager
from infrastructure.parsers.parser import ProductParser
from domain.entities.product_fields import ProductFields
from domain.entities.user import User
from application.collector import Collector

from application.use_cases.old_price import UpdatePricesUseCase
from application.use_cases.create_user import CreateUserUseCase

from domain.exceptions import UserCreateError


class ProductService:
    '''Сервисный слой для оркестрации UseCase'''

    def __init__(self):
        database = DataBaseConnection()
        uow_factory = UnitOfWorkFactory(database)
        collector = Collector(uow_factory)
        update_prices = UpdatePricesUseCase(uow_factory)

    async def create_user(self, user: User):
        '''Создать пользователя'''
        try:
            create_user = CreateUserUseCase(user)
        except UserCreateError as e:
            logger.error(f'Ошибка при создании пользователя: {e}')
            raise UserCreateError(user_id=user.id)
        except Exception as e:
            logger.error(f'Ошибка при создании пользователя: {e}')
            raise Exception(f'Ошибка при создании пользователя: {e}')
