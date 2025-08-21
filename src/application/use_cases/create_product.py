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

    def execute(self, product: Product, price: Price, user_id: str) -> None:
        try:
            # Проверяем, существует ли пользователь
            existing_user = self.user_repo.get(user_id)
            if not existing_user:
                raise ValueError(f"Пользователь {user_id} не найден")
            
            existing_product = self.product_repo.get(product.id)
            if existing_product:
                raise ValueError(f"Продукт {product.id} уже существует")

            # Сохраняем цену
            self.price_repo.save(price)
            logger.info('Цена сохранена')

            # Обновляем price_id у Продукта и сохраняем его
            product.price_id = price.id
            self.product_repo.save(product)
            logger.info(f'Товар сохранен: {product} с обновленным price_id - {price.id}')

            # Обновляем список продуктов пользователя
            existing_user.products.append(product.id)
            self.user_repo.save(existing_user)
            logger.info(f'Продукт {product.id} добавлен пользователю {existing_user.id}')
        except Exception as e:
            raise ProductCreationError(f'Ошибка создания продукта: {e}')

        