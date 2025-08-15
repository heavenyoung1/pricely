import logging
from typing import Optional

from src.application.use_cases import (
    CreateProductUseCase,
    DeleteProductUseCase,
    GetProductUseCase,
    UpdatePriceUseCase,
    CreateUserUseCase,
)
from src.domain.entities import Product, Price, User
from src.infrastructure.database.core import UnitOfWork, with_uow

logger = logging.getLogger(__name__)

class ProductService:
    '''Сервисный слой. Никаких commit здесь руками — коммитит UoW.'''
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    @with_uow(lambda self: self.uow_factory())
    def create_user(self, user: User, uow: UnitOfWork):
        use_case = CreateUserUseCase(user_repo=uow.user_repository())
        use_case.execute(user)

    @with_uow(lambda self: self.uow_factory())
    def create_product(self, user_id: str, product: Product, price: Price, uow: UnitOfWork) -> None:
        use_case = CreateProductUseCase(
            user_repo=uow.user_repository(),
            product_repo=uow.product_repository(),
            price_repo=uow.price_repository(),
        )
        use_case.execute(user_id, product, price)

    @with_uow(lambda self: self.uow_factory(), commit=False)
    def get_product(self, product_id: str, uow: UnitOfWork) -> Optional[Product]:
        use_case = GetProductUseCase(product_repo=uow.product_repository())
        use_case.execute(product_id=product_id)

        













    # @with_uow(lambda self: self.uow_factory())  # commit=True по умолчанию
    # def create(self, product: Product, price: Price, user: User, uow: UnitOfWork) -> None:
    #     use_case = CreateProductUseCase(
    #         product_repo=uow.product_repository(),
    #         price_repo=uow.price_repository(),
    #         user_repo=uow.user_repository(),
    #     )
    #     use_case.execute(product, price, user)

    # @with_uow(lambda self: self.uow_factory())  # commit=True по умолчанию
    # def delete(self, product_id: str, uow: UnitOfWork) -> bool:
    #     use_case = DeleteProductUseCase(
    #         product_repo=uow.product_repository(),
    #         )
    #     return use_case.execute(product_id)

    # @with_uow(lambda self: self.uow_factory())  # commit=True по умолчанию
    # def get(self, product_id: str, uow: UnitOfWork) -> Optional['Product']:
    #     use_case = GetProductUseCase(
    #         product_repo=uow.product_repository(),
    #     )
    #     return use_case.execute(product_id)

    # @with_uow(lambda self: self.uow_factory())  # commit=True по умолчанию
    # def update(self, price: Price , product_id: str, uow: UnitOfWork) -> None:
    #     use_case = UpdatePriceUseCase(
    #         product_repo=uow.product_repository(),
    #         price_repo=uow.price_repository(),
    #     )
    #     use_case.execute(price , product_id)

