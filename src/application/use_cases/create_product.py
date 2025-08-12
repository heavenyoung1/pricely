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
        '''Создаёт продукт, цену и обновляет пользователя.

        Args:
            product (Product): Создаваемый продукт
            price (Price): Начальная цена продукта
            user (User): Владелец продукта

        Raises:
            ProductCreationError: Если не удалось создать продукт, цену или обновить пользователя
        '''
        try:
            # Проверяем, существует ли пользователь
            existing_user = self.user_repo.get(user.id)
            if not existing_user:
                raise ProductCreationError(f'Пользователь с id {user.id} не найден')

            # Сохраняем цену
            self.price_repo.save(price)
            logger.info('Цена сохранена')

            # Обновляем price_id у Продукта (Product) и сохраняем его
            product.price_id = price.id
            self.product_repo.save(product)
            logger.info('Продукт сохранен: {product}')

            # Если продукта нет у пользователя — добавляем
            #if product.id not in user.products:
            user.products.append(product.id)
            self.user_repo.save(user) # нужен ли этот шаг??
            logger.info('Продукт {product.id} добавлен пользователю {user.id}') 

        except Exception as e:
            raise ProductCreationError(f'Ошибка создания продукта: {e}')

        