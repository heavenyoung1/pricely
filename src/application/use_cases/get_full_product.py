import logging
from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError

logger = logging.getLogger(__name__)


class GetFullProductUseCase:
    def __init__(
        self,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        user_repo: UserRepository
    ):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo

    def execute(self, product_id: str):
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning(f'Товар {product_id} не найден')
            raise ProductNotFoundError(f'Товар {product_id} не существует')

        #price = None Я забыл зачем это здесь, позже удалить
        if product.price_id:
            price = self.price_repo.get(product.price_id)

        user = self.user_repo.get(product.user_id)
        if not user:
            logger.warning(f'Пользователь {product.user_id} не найден для товара {product_id}')

        logger.info(f'Успешно получена информация о товаре {product_id}')
        return {
            'product': product,
            'price': price,
            'user': user,
        }

