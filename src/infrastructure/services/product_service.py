import logging
from typing import Optional, Dict
from src.application.exceptions import ProductNotFoundError, PriceUpdateError, ProductCreationError
from src.infrastructure.core.ozon_parser import OzonParser
from src.application.exceptions import *
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
    '''Сервисный слой для оркестрации UseCase с использованием UnitOfWork.'''
    def __init__(self, uow_factory):
        self.uow_factory = uow_factory

    @with_uow(commit=True)
    def create_user(self, user: User, uow: UnitOfWork) -> None:
        try:
            use_case = CreateUserUseCase(user_repo=uow.user_repository())
            use_case.execute(user)
        except Exception as e:
            logger.error(f'Ошибка при создании пользователя {user.id}: {str(e)}')
            raise

    @with_uow(commit=True)
    def create_product(self, user_id: str, url: str, uow: UnitOfWork) -> str:
        try:
            use_case = CreateProductUseCase(
                user_repo=uow.user_repository(),
                product_repo=uow.product_repository(),
                price_repo=uow.price_repository(),
                parser=OzonParser(),
            )
            return use_case.execute(user_id, url)
        except ProductCreationError as e:
            logger.warning(f'Ошибка создания продукта для пользователя {user_id}: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Неизвестная ошибка при создании продукта: {str(e)}')
            raise

    @with_uow(commit=False)
    def get_product(self, product_id: str, uow: UnitOfWork) -> Product:
        try:
            use_case = GetProductUseCase(product_repo=uow.product_repository())
            return use_case.execute(product_id)
        except ProductNotFoundError as e:
            logger.warning(f'Продукт {product_id} не найден: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Ошибка при получении продукта {product_id}: {str(e)}')
            raise

    @with_uow(commit=False)
    def get_full_product(self, product_id: str, uow: UnitOfWork):
        try:
            use_case = GetFullProductUseCase(
                product_repo=uow.product_repository(),
                price_repo=uow.price_repository(),
                user_repo=uow.user_repository(),
            )
            return use_case.execute(product_id)
        except ProductNotFoundError as e:
            logger.warning(f'Продукт {product_id} не найден: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Ошибка при получении полной информации о продукте {product_id}: {str(e)}')
            raise

    @with_uow(commit=True)
    def update_product_price(self, product_id: str, price: Price, uow: UnitOfWork) -> None:
        try:
            use_case = UpdateProductPriceUseCase(
                product_repo=uow.product_repository(),
                price_repo=uow.price_repository(),
            )
            use_case.execute(product_id, price)
            logger.de
        except Exception as e:
            logger.error(f'Ошибка при обновлении цены: {e}')

    @with_uow(commit=True)
    def delete_product(self, product_id, uow: UnitOfWork) -> None:
        try:
            use_case = DeleteProductUseCase(
                user_repo=uow.user_repository(),
                product_repo=uow.product_repository(),
                price_repo=uow.price_repository(),
        )
            use_case.execute(product_id)
        except ProductNotFoundError as e:
            logger.warning(f'Продукт {product_id} не найден: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Ошибка при удалении продукта {product_id}: {str(e)}')
            raise