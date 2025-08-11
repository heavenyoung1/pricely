import logging
from typing import Optional, TYPE_CHECKING

from src.application.use_cases import CreateProductUseCase
from src.application.use_cases import DeleteProductUseCase
from src.application.use_cases import GetProductUseCase
from src.application.use_cases import UpdatePriceUseCase
from src.infrastructure.database.core.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from src.domain.entities import Product

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, uow_factory):
        '''
        uow_factory — функция или класс, создающий UnitOfWork.
        Например: lambda: UnitOfWork()
        '''
        self.uow_factory = uow_factory

    def create_product_with_price(self, product, price, user) -> None:
        '''Создать товар с ценой и обновить пользователя.'''
        with self.uow_factory as uow:
            use_case = CreateProductUseCase(
                product_repo=uow.product_repository(),
                price_repo=uow.price_repository(),
                user_repo=uow.user_repository(),
            )
            use_case.execute(product, price, user)
            uow.commit()

    def delete_product(self, product_id) -> None:
        '''Удалить товар.'''
        with self.uow_factory as uow:
            use_case = DeleteProductUseCase(
                product_repo=uow.product_repository(),
            )
        use_case.execute(product_id)
        uow.commit()

    def get_product(self, product_id) -> Optional['Product']:
        '''Получить товар.'''
        with self.uow_factory as uow:
            use_case = GetProductUseCase(
                product_repo=uow.product_repository(),
            )
        use_case.execute(product_id)

    def update_price(self, price , product_id) -> None:
        '''Обновить цену товара.'''
        with self.uow_factory as uow:
            use_case = UpdatePriceUseCase(
                product_repo=uow.product_repository(),
                price_repo=uow.price_repository(),
            )
            use_case.execute(price , product_id)
            uow.commit()


    
    