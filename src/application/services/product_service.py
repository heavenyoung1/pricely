import logging
import json

from src.domain.entities import Product, Price, User
from src.interfaces.repositories import ProductRepository, PriceRepository, UserRepository

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(
            self, 
            product_repository: ProductRepository,
            price_repository: PriceRepository,
            user_repository: UserRepository,
    ):
        self.product_repository = product_repository
        self.price_repository = price_repository
        self.user_repository = user_repository

    def create_product(self, product: Product, price: Price, user: User) -> Product:
        '''Создаёт или обновляет продукт, цену и пользователя.'''

        # Сохраняем цену в PRICE
        self.price_repository.save_price(price)
        logger.info(f'Цена сохранена')

        # Обновляем PRICE_ID в PRODUCT 
        product.price_id = price.id
        self.product_repository.save_product(product)
        logger.info(f'Объект PRODUCT обновлен или сохранен')

        product_ids= json.loads(user.products)
        if product.id not in product_ids:
            product_ids.append(product.id)
            user.products = json.dumps(product_ids)
            logger.info(f'ID Товара добавлен в список к Пользователю')






        
