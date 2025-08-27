import logging
from typing import Optional, Dict

from src.application.use_cases import (
    CreateUserUseCase,
    CreateProductUseCase,
    GetProductUseCase,
    GetFullProductUseCase,
    UpdateProductPriceUseCase,
    DeleteProductUseCase,
)

from src.domain.entities import Product, Price, User
from src.infrastructure.database.core import UnitOfWork, with_uow

logger = logging.getLogger(__name__)

class ProductService:
    '''Сервисный слой. Никаких commit здесь руками — коммитит UoW.'''
    def __init__(
        self,
        uow_factory,
        create_user_use_case: CreateUserUseCase,
        create_product_use_case: CreateProductUseCase,
        get_product_use_case: GetProductUseCase,
        get_full_product_use_case: GetFullProductUseCase,
        update_product_price_use_case: UpdateProductPriceUseCase,
        delete_product_use_case: DeleteProductUseCase
        ):
        self.uow_factory = uow_factory
        self.create_user_use_case = create_user_use_case
        self.create_product_use_case = create_product_use_case
        self.get_product_use_case = get_product_use_case
        self.get_full_product_use_case = get_full_product_use_case
        self.update_product_price_use_case = update_product_price_use_case
        self.delete_product_use_case = delete_product_use_case

    @with_uow(commit=True)
    def create_user(self, user: User, uow: UnitOfWork):
        use_case = CreateUserUseCase(user_repo=uow.user_repository())
        use_case.execute(user)

    @with_uow(commit=True)
    def create_product(self, user_id: str, url: str , uow: UnitOfWork) -> None:
        use_case = CreateProductUseCase(
            user_repo=uow.user_repository(),
            product_repo=uow.product_repository(),
            price_repo=uow.price_repository(),
        )
        return use_case.execute(user_id, url)

    @with_uow(commit=False)
    def get_product(self, product_id: str, uow: UnitOfWork) -> Optional[Product]:
        use_case = GetProductUseCase(product_repo=uow.product_repository())
        use_case.execute(product_id)

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
        use_case.execute(product_id, price)

    @with_uow(commit=False)
    def delete_product(self, product_id, uow: UnitOfWork) -> None:
        use_case = DeleteProductUseCase(
            user_repo=uow.user_repository(),
            product_repo=uow.product_repository(),
            price_repo=uow.price_repository(),
        )
        use_case.execute(product_id)