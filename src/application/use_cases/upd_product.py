import logging
from src.domain.repositories import ProductRepository, PriceRepository
from src.domain.entities import Product, Price

logger = logging.getLogger(__name__)

class UpdateProductPriceUseCase:
    def __init__(self, product_repo: ProductRepository, price_repo: PriceRepository):
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, product: Product, price: Price) -> None:
        product = self.product_repo.get(product.id)
        if not product:
            raise ValueError('Продукт не найден')

        # 1) сохраняем новую цену
        self.price_repo.save(price)
        # 2) обновляем price_id в продукте
        product.price_id = price.id
        self.product_repo.save(product)
