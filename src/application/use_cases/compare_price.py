from src.application.interfaces.repositories import ProductRepository, PriceRepository
from src.infrastructure.notifications.notification_service import NotificationService
from src.infrastructure.parsers import OzonParser
from src.domain.entities import Price
from src.domain.exceptions import PriceUpdateError
import logging

logger = logging.getLogger(__name__)

class CompareProductPriceUseCase:
    '''Use Case для сравнения цены товара с актуальной ценой на сайте.'''

    def __init__(self, product_repo: ProductRepository, price_repo: PriceRepository, parser: OzonParser, notification_service: NotificationService):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.parser = parser
        self.notification_service = notification_service

    def execute(self, product_id: str) -> None:
        try:
            # Получаем продукт
            product = self.product_repo.get(product_id)
            if not product:
                raise PriceUpdateError(f"Продукт с ID {product_id} не найден.")

            # Получаем актуальную цену с сайта
            product_data = self.parser.parse_product(product.link)
            current_price = product_data['price_with_card']

            # Получаем последнюю цену из базы
            latest_price = self.price_repo.get_latest_for_product(product_id)
            if not latest_price:
                raise PriceUpdateError(f"Цены для продукта {product_id} не найдены.")

            # Сравниваем цены
            if current_price != latest_price.with_card:
                # Цена изменилась, обновляем цену в базе
                latest_price.with_card = current_price
                self.price_repo.save(latest_price)

                # Уведомляем пользователя
                self.notification_service.send_price_update_notification(product.user_id, product.name, current_price)

        except Exception as e:
            logger.error(f"Ошибка при сравнении цены для товара {product_id}: {str(e)}")
            raise PriceUpdateError(f"Ошибка при сравнении цены для товара {product_id}: {str(e)}")
