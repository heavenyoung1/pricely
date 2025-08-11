import logging
from src.domain.entities import Product, Price, User
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository

logger = logging.getLogger(__name__)

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
        # Сохраняем цену
        self.price_repo.save(price)
        logger.info('Цена сохранена')

        # Обновляем price_id у Товара (Product) и сохраняем его
        product.price_id = price.id
        self.product_repo.save(product)
        logger.info('Продукт сохранен')

        # Если продукта нет у пользователя — добавляем
        if product.id not in user.products:
            user.products.append(product.id)
            self.user_repo.save(user) # нужен ли этот шаг??
            logger.info('Товар добавлен пользователю') 

        