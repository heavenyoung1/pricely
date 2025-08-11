import logging
from typing import Optional, TYPE_CHECKING

from src.application.use_cases import (
    CreateProductUseCase,
    DeleteProductUseCase,
    GetProductUseCase,
    UpdatePriceUseCase
)

from src.infrastructure.database.core.unit_of_work import UnitOfWork

if TYPE_CHECKING:
    from src.domain.entities import Product

logger = logging.getLogger(__name__)

class ProductService:
    '''Сервис для управления товарами и их ценами.
    
    Обеспечивает:
    - Создание товаров с ценами
    - Удаление товаров
    - Получение информации о товарах
    - Обновление цен
    '''

    def __init__(self, uow_factory):
        '''Инициализирует сервис.
        
        Args:
            uow_factory (Callable[[], UnitOfWork]): Фабрика для создания UoW'''
        self.uow_factory = uow_factory

    def create_product_with_price(self, product, price, user) -> None:
        '''Создает новый продукт с ценой и связывает с пользователем.
        
        Args:
            product (Product): Создаваемый продукт
            price (Price): Начальная цена продукта
            user (User): Владелец продукта
            
        Raises:
            ProductCreationError: Если не удалось создать продукт.'''
        with self.uow_factory() as uow:
            use_case = CreateProductUseCase(
                product_repo=uow.product_repository(),
                price_repo=uow.price_repository(),
                user_repo=uow.user_repository(),
            )
            use_case.execute(product, price, user)
            uow.commit()

    def delete_product(self, product_id) -> None:
        '''Удаляет продукт по его идентификатору.
        
        Args:
            product_id (str): ID удаляемого продукта
            
        Raises:
            ProductNotFoundError: Если продукт не существует.
        '''
        with self.uow_factory() as uow:
            use_case = DeleteProductUseCase(
                product_repo=uow.product_repository(),
            )
            use_case.execute(product_id)
            uow.commit()

    def get_product(self, product_id) -> Optional['Product']:
        '''Получает информацию о продукте.
        
        Args:
            product_id (str): ID запрашиваемого продукта
            
        Returns:
            Optional[Product]: Найденный продукт или None.
        '''
        with self.uow_factory() as uow:
            use_case = GetProductUseCase(
                product_repo=uow.product_repository(),
            )
        use_case.execute(product_id)

    def update_price(self, price , product_id) -> None:
        '''Обновляет цену для указанного продукта.
        
        Args:
            price (Price): Новая цена
            product_id (str): ID продукта
            
        Raises:
            PriceUpdateError: Если не удалось обновить цену.
        '''
        with self.uow_factory() as uow:
            use_case = UpdatePriceUseCase(
                product_repo=uow.product_repository(),
                price_repo=uow.price_repository(),
            )
            use_case.execute(price , product_id)
            uow.commit()


    
    