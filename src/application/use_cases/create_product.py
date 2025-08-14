import logging
from src.domain.entities import Product, Price, User
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository

logger = logging.getLogger(__name__)

class ProductCreationError(Exception):
    '''Исключение для ошибок при создании продукта.'''
    pass

class CreateProductUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        user_repo: UserRepository,
    ):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo

    def execute(self, product: Product, price: Price, user: User) -> None:
        '''
        Алгоритм (одна транзакция через UoW):
        1) Проверяем пользователя
        2) Сохраняем цену
        3) Проставляем product.price_id и сохраняем продукт
        4) Добавляем product.id в user.products и сохраняем пользователя
        '''
        try:
            existing_user = self.user_repo.get(user.id)
            if not existing_user:
                raise ProductCreationError(f'Пользователь с id {user.id} не найден')

            self.price_repo.save(price)
            logger.info('Цена сохранена')

            product.price_id = price.id
            self.product_repo.save(product)
            logger.info(f'Продукт сохранен: {product}')

            # гарантируем сохранение связи user -> product
            existing_user.products = list(existing_user.products or [])
            if product.id not in existing_user.products:
                existing_user.products.append(product.id)
                self.user_repo.save(existing_user)

            logger.info(f'Продукт {product.id} добавлен пользователю {user.id}')

        except Exception as e:
            raise ProductCreationError(f'Ошибка создания продукта: {e}')

        