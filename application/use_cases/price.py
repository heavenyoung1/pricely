from infrastructure.database.unit_of_work import UnitOfWorkFactory

from application.tools.adapter import LinkAdapter
from domain.exceptions import PropductCreateError
from core.logger import logger

from domain.entities.product import Product
from domain.entities.price import Price
from domain.entities.user import User

class CreatePrice:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(
            self, 
            product,
            price, 
            user
            ):
        async with self.uow_factory.create() as uow: