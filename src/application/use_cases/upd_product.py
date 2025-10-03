import logging
from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product, Price
from src.domain.exceptions import ProductNotFoundError, PriceUpdateError
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class UpdateProductPriceUseCase:
    def __init__(self, product_repo: ProductRepository, price_repo: PriceRepository):
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, product_id: str, with_card: int, without_card: int) -> Product:
        """
        Обновляет цену товара:
        - ищет продукт,
        - берёт последнюю цену,
        - создаёт новую,
        - сохраняет в БД,
        - возвращает обновлённый продукт.
        """
        product = self.product_repo.get(product_id)
        if not product:
            raise ValueError(f"Товар {product_id} не найден")

        latest = self.price_repo.get_latest_for_product(product_id)

        new_price = Price(
            id=None,  # БД сама создаст автоинкрементный id
            product_id=product_id,
            with_card=with_card,
            without_card=without_card,
            previous_with_card=latest.with_card if latest else None,
            previous_without_card=latest.without_card if latest else None,
            created_at=datetime.now()
        )

        self.price_repo.save(new_price)

        # подтянем цены в объект продукта
        product.prices.append(new_price)

        logger.info(f"Цена для товара {product_id} обновлена: {new_price}")
        return product
