import logging
from typing import Optional, Dict

from src.application.use_cases import (
    CreateUserUseCase,
    CreateProductUseCase,
    GetProductUseCase,
    GetFullProductUseCase,
    UpdatePriceUseCase,
    DeleteProductUseCase,
)

from src.domain.entities import Product, Price, User
from src.infrastructure.database.core import UnitOfWork, with_uow

logger = logging.getLogger(__name__)

class ProductService:
    '''Сервисный слой. Никаких commit здесь руками — коммитит UoW.'''
    def __init__(self, uow_factory=None):
        self.uow_factory = uow_factory

    @with_uow(commit=True)
    def create_user(self, user: User, uow: UnitOfWork):
        use_case = CreateUserUseCase(user_repo=uow.user_repository())
        use_case.execute(user)

    @with_uow(commit=True)
    def create_product(self, user_id: str, product: Product, price: Price, uow: UnitOfWork) -> None:
        use_case = CreateProductUseCase(
            user_repo=uow.user_repository(),
            product_repo=uow.product_repository(),
            price_repo=uow.price_repository(),
        )
        use_case.execute(product, price, user_id)

    @with_uow(commit=False)
    def get_product(self, product_id: str, uow: UnitOfWork) -> Optional[Product]:
        use_case = GetProductUseCase(product_repo=uow.product_repository())
        use_case.execute(product_id=product_id)

    @with_uow(commit=False)
    def get_full_product(self, product_id, uow: UnitOfWork) -> Optional[Dict]:
        use_case = GetFullProductUseCase(
            user_repo=uow.user_repository(),
            product_repo=uow.product_repository(),
            price_repo=uow.price_repository(),
        )
        use_case.execute(product_id)

    @with_uow(commit=False)
    def update_product_price(self, product_id, price: Price, uow: UnitOfWork) -> None:
        use_case = UpdatePriceUseCase(
            product_repo=uow.product_repository(),
            price_repo=uow.price_repository(),
        )
        use_case.execute(price, product_id)

    @with_uow(commit=False)
    def delete_product(self, product_id, uow: UnitOfWork) -> None:
        use_case = DeleteProductUseCase(
            user_repo=uow.user_repository(),
            product_repo=uow.product_repository(),
            price_repo=uow.price_repository(),
        )
        use_case.execute(product_id)