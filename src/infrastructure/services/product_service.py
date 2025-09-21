import logging
from typing import Optional, Dict
from src.domain.exceptions import ProductNotFoundError, PriceUpdateError, ProductCreationError
from src.infrastructure.parsers import OzonParser
from src.application.use_cases import (
    CreateUserUseCase,
    CreateProductUseCase,
    GetProductUseCase,
    GetFullProductUseCase,
    UpdateProductPriceUseCase,
    DeleteProductUseCase,
)

from src.domain.exceptions import (
    ProductNotFoundError, PriceUpdateError, ProductCreationError,
    UserCreationError, ParserProductError, ProductDeletingError
)

from src.domain.entities import Product, Price, User
from src.core import SQLAlchemyUnitOfWork, with_uow

logger = logging.getLogger(__name__)

class ProductService:
    '''Сервисный слой для оркестрации UseCase с использованием UnitOfWork.'''
    def __init__(self, uow_factory, parser: Optional[OzonParser] = None):
        self.uow_factory = uow_factory
        self.parser = parser or OzonParser()  # дефолт = OzonParser

    @with_uow(commit=True)
    def create_user(self, user: User) -> None:
        try:
            use_case = CreateUserUseCase(user_repo=self.uow.user_repository)
            use_case.execute(user)
        except Exception as e:
            logger.error(f'Ошибка при создании пользователя {user.id}: {str(e)}')
            raise UserCreationError(f"Ошибка создания пользователя: {str(e)}")

    @with_uow(commit=True)
    def create_product(self, user_id: str, url: str) -> dict:
        use_case = CreateProductUseCase(
            user_repo=self.uow.user_repository,
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            parser=self.parser,
        )
        return use_case.execute(user_id, url)

    @with_uow(commit=False)
    def get_product(self, product_id: str) -> Product:
        try:
            use_case = GetProductUseCase(product_repo=self.uow.product_repository)
            return use_case.execute(product_id)
        except ProductNotFoundError as e:
            logger.warning(f'Продукт {product_id} не найден: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Ошибка при получении продукта {product_id}: {str(e)}')
            raise

    @with_uow(commit=False)
    def get_full_product(self, product_id: str):
        try:
            use_case = GetFullProductUseCase(
                product_repo=self.uow.product_repository,
                price_repo=self.uow.price_repository,
                user_repo=self.uow.user_repository,
            )
            return use_case.execute(product_id)
        except ProductNotFoundError as e:
            logger.warning(f'Продукт {product_id} не найден: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Ошибка при получении полной информации о продукте {product_id}: {str(e)}')
            raise

    def get_all_product(self, user_id: str) -> list:
        try:
            self.uow.user_repository.get(user_id)
            if not user_id:
                logger.warning(f'Пользователь {user_id} не найден')
                return None
            else:
                # достаём все продукты пользователя
                products_id = [for product in self.user_]

        except Exception as e:
            logger.error(f'Ошибка при получении пользователя {user_id}: {str(e)}')
            raise

    @with_uow(commit=True)
    def update_product_price(self, product_id: str, price: Price) -> None:
        try:
            use_case = UpdateProductPriceUseCase(
                product_repo=self.uow.product_repository,
                price_repo=self.uow.price_repository,
            )
            use_case.execute(product_id, price)
            logger.debug(f'Цена для продукта {product_id} успешно обновлена')
        except Exception as e:
            logger.error(f'Ошибка при обновлении цены: {e}')

    @with_uow(commit=True)
    def delete_product(self, product_id) -> None:
        try:
            use_case = DeleteProductUseCase(
                user_repo=self.uow.user_repository,
                product_repo=self.uow.product_repository,
                price_repo=self.uow.price_repository,
        )
            use_case.execute(product_id)
        except ProductNotFoundError as e:
            logger.warning(f'Продукт {product_id} не найден: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Ошибка при удалении продукта {product_id}: {str(e)}')
            raise