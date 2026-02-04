from typing import List

from infrastructure.database.unit_of_work import UnitOfWorkFactory
from domain.entities.product import Product


class GetUserProductsUseCase:
    '''Use case для получения всех товаров пользователя.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, user_id: int) -> List[Product]:
        '''
        Получает список всех товаров, отслеживаемых пользователем.

        Args:
            user_id: Идентификатор пользователя.

        Returns:
            Список товаров пользователя.
        '''
        async with self.uow_factory.create() as uow:
            product_ids = await uow.user_products_repo.get_all_by_user(user_id)
            products = await uow.product_repo.get_many(product_ids)
            return products
