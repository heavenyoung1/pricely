import logging
from src.domain.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Price

logger = logging.getLogger(__name__)


class UpdatePriceUseCase:
    def __init__(self, product_repo: ProductRepository, price_repo: PriceRepository):
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, price: Price, product_id: str) -> None:
        # 1) Сохраняем цену
        self.price_repo.save(price)

        # 2) Обновляем продукт
        product = self.product_repo.get(product_id)
        if not product:
            raise ValueError(f'Продукт с id {product_id} не найден')

        product.price_id = price.id
        self.product_repo.save(product)
        logger.info(f'Цена обновлена для продукта {product_id} -> price_id={price.id}')