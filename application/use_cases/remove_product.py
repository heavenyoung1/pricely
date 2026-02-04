from infrastructure.database.unit_of_work import UnitOfWorkFactory
from domain.exceptions import ProductNotFoundError
from core.logger import logger


class RemoveProductUseCase:
    '''Use case для удаления товара из системы.'''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def execute(self, product_id: int) -> bool:
        '''
        Удаляет товар и все связанные данные (цены, связи с пользователями).

        Args:
            product_id: Идентификатор товара для удаления.

        Returns:
            True при успешном удалении.

        Raises:
            ProductNotFoundError: Если товар не найден.
        '''
        async with self.uow_factory.create() as uow:
            existing = await uow.product_repo.get(product_id)
            if not existing:
                raise ProductNotFoundError(product_id)

            # Каскадное удаление: prices и user_products удалятся автоматически
            await uow.product_repo.delete(product_id)
            logger.info(f'Товар {product_id} успешно удалён')
            return True
