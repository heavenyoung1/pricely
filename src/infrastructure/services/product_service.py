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
from src.infrastructure.notifications.notification_service import NotificationService

logger = logging.getLogger(__name__)

class ProductService:
    '''Сервисный слой для оркестрации UseCase с использованием UnitOfWork.'''
    def __init__(self, uow_factory, parser: Optional[OzonParser] = None, bot=None):
        self.uow_factory = uow_factory
        self.parser = parser or OzonParser()  # дефолт = OzonParser
        self.notification_service = NotificationService(bot)

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
            user_products_repo = self.uow.user_products_repository,
            parser=self.parser,
        )
        return use_case.execute(user_id, url)

    @with_uow(commit=False)
    # Можно все эти исключения перенести в UseCase!!!!
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

    @with_uow(commit=False)
    def get_all_products(self, user_id: str) -> list:
        '''Возвращает список словарей с полной информацией обо всех продуктах пользователя.'''
        use_case_get_products = GetProductForUserUseCase (
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            user_products_repo=self.uow.user_products_repository
        )
        product_refs = use_case_get_products.execute(user_id=user_id)
        if not product_refs:
            return []
        
        # Если use_case вернул уже готовые dict'ы с данными — просто вернём их
        if isinstance(product_refs, list) and product_refs and isinstance(product_refs[0], dict):
            return product_refs

        # Иначе ожидаем список идентификаторов (str) и подгружаем полные карточки
        use_case_for_products = GetFullProductUseCase(
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            user_repo=self.uow.user_repository,
        )

        products = []
        for pid in product_refs:
            try:
                # защита: приведение к строке
                pid_str = str(pid)
                product_full = use_case_for_products.execute(pid_str)
                products.append(product_full)
            except ProductNotFoundError:
                logger.warning(f"Product {pid} is referenced for user {user_id} but not found in products table")
            except Exception as e:
                logger.error(f"Ошибка получения полной карточки для {pid}: {e}")
                
        return products

    @with_uow(commit=True)
    def update_product_price(self, product_id: str) -> dict:
        """
        Парсит цену, сохраняет в БД и возвращает полную карточку товара (dict).
        """
        use_case_update_product = UpdateProductPriceUseCase(
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            parser=OzonParser(),
        )

        result_use_case_update_product = use_case_update_product.execute(
            product_id=product_id,
        )
        is_changed = result_use_case_update_product['is_changed']
        # ===============================
        #Перезапишу туту 
        # Вернём полную карточку в dict-формате (как get_full_product)
        use_case_get_full_product = GetFullProductUseCase(
            product_repo=self.uow.product_repository,
            price_repo=self.uow.price_repository,
            user_repo=self.uow.user_repository,
        )
        
        result_use_case_update_product = use_case_update_product.execute(product_id)
        if result_use_case_update_product['is_changed']:
            result_use_case_get_full_product = use_case_get_full_product.execute(product_id)
            return {
                "updated_product": result_use_case_get_full_product['data_return']['product_data'],
                "is_changed": is_changed,
            }
        return {"updated_product": None, "is_changed": is_changed}


    @with_uow(commit=False)
    def get_all_products_for_update(self):
        """
        Возвращает список всех товаров, которые нужно обновлять.
        Можно потом добавить фильтры (например, активные пользователи).
        """
        use_case = GetUserProductsUseCase(
            user_products_repo=self.uow.user_products_repository
        )
        return use_case.execute()

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

# Инициализация сервиса
# Правильно ли так делать и объявлять его здесь?
product_service = ProductService(uow_factory=SQLAlchemyUnitOfWork)