import logging
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository

logger = logging.getLogger(__name__)


class DeleteProductUseCase:
    def __init__(self, user_repo: UserRepository, product_repo: ProductRepository, price_repo: PriceRepository):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, product_id: str) -> None:
        product = self.product_repo.get(product_id)
        if not product:
            return

        # удалить цену
        if product.price_id:
            self.price_repo.delete(product.price_id)

        # удалить товар
        self.product_repo.delete(product_id)

        # удалить связь у пользователя
        user = self.user_repo.get(product.user_id)
        if user and product_id in user.products:
            user.products.remove(product_id)
            self.user_repo.save(user)
        logger.info(f'Операция удаления выполнена для ID {product_id}')