import logging
from typing import Optional
from src.domain.exceptions import ProductNotFoundError, UserCreationError
from src.infrastructure.parsers import OzonParser
from src.application.use_cases import (
    CreateUserUseCase,
    CreateProductUseCase,
    GetProductUseCase,
    GetFullProductUseCase,
    UpdateProductPriceUseCase,
    DeleteProductUseCase,
    GetProductForUserUseCase,
    GetUserProductsUseCase,
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
        '''Создает нового пользователя.'''
        try:
            use_case = CreateUserUseCase(user_repo=self.uow.user_repository)
            use_case.execute(user)
        except Exception as e:
            logger.error(f'Ошибка при создании пользователя {user.id}: {str(e)}')
            raise UserCreationError(f'Ошибка создания пользователя: {str(e)}')

    @with_uow(commit=True)
    def create_product(self, user_id: str, url: str) -> dict:
        '''Создает новый товар по URL.'''
        use_case = CreateProductUseCase(
            user_repo=self.uow.user_repository,
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            user_products_repo=self.uow.user_products_repository,
            parser=self.parser,
        )
        return use_case.execute(user_id, url)

    @with_uow(commit=False)
    def get_product(self, product_id: str) -> Product:
        '''Получить товар по ID.'''
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
        '''Получить полную информацию о товаре.'''
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

    @with_uow(commit=False)
    def get_all_products(self, user_id: str) -> list:
        '''Возвращает все продукты пользователя.'''
        use_case_get_products = GetProductForUserUseCase(
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            user_products_repo=self.uow.user_products_repository
        )
        product_refs = use_case_get_products.execute(user_id=user_id)
        if not product_refs:
            return []

        if isinstance(product_refs, list) and product_refs and isinstance(product_refs[0], dict):
            return product_refs

        use_case_for_products = GetFullProductUseCase(
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            user_repo=self.uow.user_repository,
        )

        products = []
        for pid in product_refs:
            try:
                pid_str = str(pid)
                product_full = use_case_for_products.execute(pid_str)
                products.append(product_full)
            except ProductNotFoundError:
                logger.warning(f'Product {pid} is referenced for user {user_id} but not found in products table')
            except Exception as e:
                logger.error(f'Ошибка получения полной карточки для {pid}: {e}')
                
        return products

    @with_uow(commit=True)
    def update_product_price(self, product_id: str) -> dict:
        '''Обновляет цену товара и возвращает полную карточку товара.'''
        use_case_update_product = UpdateProductPriceUseCase(
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            parser=OzonParser(),
        )

        result_use_case_update_product = use_case_update_product.execute(
            product_id=product_id,
        )

        is_changed = result_use_case_update_product['is_changed']
        updated_product = result_use_case_update_product['product_data']

        # ======================================================
        # 🧪 ДЛЯ ПРОДАКШНА ЗАКОММЕНТИРОВАТЬ СТРОКУ
        # Если is_chaned == True сообщения об изменении цены будут приходить всегда
        # is_changed = True
        # ======================================================

        return {'updated_product': updated_product, 'is_changed': is_changed}

    @with_uow(commit=False)
    def get_all_products_for_update(self):
        '''Возвращает список всех товаров, которые нужно обновлять.'''
        use_case = GetUserProductsUseCase(
            user_products_repo=self.uow.user_products_repository
        )
        return use_case.execute()

    @with_uow(commit=True)
    def delete_product(self, product_id) -> None:
        '''Удаляет продукт.'''
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

# Инициализация сервиса
product_service = ProductService(uow_factory=SQLAlchemyUnitOfWork)