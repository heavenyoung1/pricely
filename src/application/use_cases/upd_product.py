import logging
from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.entities import Product, Price
from src.domain.exceptions import ProductNotFoundError, PriceUpdateError
from src.infrastructure.parsers.ozon_parser import OzonParser
from datetime import datetime

logger = logging.getLogger(__name__)


class UpdateProductPriceUseCase:
    def __init__(self, product_repo: ProductRepository, price_repo: PriceRepository, parser: OzonParser):
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.parser = parser

    def execute(self, product_id: str, with_card: int, without_card: int) -> Product:
        """
        Обновляет цену товара:
        - ищет продукт,
        - берёт последнюю цену,
        - создаёт новую,
        - сохраняет в БД,
        - возвращает обновлённый продукт.
        """
        # Формируем флаг для отслеживания изменения цены
        is_changed: bool = False

        try:
            # 1. Берем текущий продукт
            product = self.product_repo.get(product_id)
            if not product:
                raise ProductNotFoundError(f"Товар {product_id} не найден")

            # 2. Достаём последние цены из БД (with_card, without_card), именно они нужны для дальнейшей бизнес-логики
            last_price = self.price_repo.get_latest_for_product(product_id)

            previous_price_with_card = last_price.with_card if last_price else None
            previous_price_without_card = last_price.without_card if last_price else None

            # 3. Парсим новые данные
            try:
                product_data = self.parser.parse_product(product.link)
            except Exception as e:
                logger.error(f"Ошибка при парсинге данных для товара {product_id}: {e}")
                raise PriceUpdateError(f"Ошибка при парсинге данных для товара {product_id}")

            # Создаем новую доменную сущность - цену
            price = Price(
                id=None,  # БД сама создаст автоинкрементный id
                product_id=product.id,
                with_card=product_data['price_with_card'],
                without_card=product_data['price_without_card'],
                previous_with_card=previous_price_with_card,
                previous_without_card=previous_price_without_card,
                created_at=datetime.now(),
            )
            # потом удалить ,хочу посмотреть что там лежит!!!
            logger.info(f'DEBUG!!! PRICE -> {price}')
            logger.info(f'DEBUG!!! PRICE.WITH_CARD -> {price.previous_with_card}')

            # Сохраняем цену в БД
            try:
                self.price_repo.save(price)
            except Exception as e:
                logger.error(f'Ошибка обновления цены: {e}')
                raise PriceUpdateError(f'Ошибка обновления цены')

            # Заводим переменные для удобного взаимодействия
            actual_price_with_card = price.with_card
            actual_price_without_card = price.without_card

            # Проверяем, изменились ли цены
            if (actual_price_with_card != previous_price_with_card) or (actual_price_without_card != previous_price_without_card):
                is_changed = True

            # Возвращаем данные для UI и флаг is_changed
            return {
                "id": product.id,
                "name": product.name,
                "link": product.link,
                "with_card": actual_price_with_card,
                "without_card": actual_price_without_card,
                "previous_price_with_card": previous_price_with_card,
                "previous_price_without_card": previous_price_without_card,
                "is_changed": is_changed  # Флаг, сообщить ли боту о изменении
            }    
            
        except ProductNotFoundError as e:
            logger.error(f"Ошибка при обновлении цены: {str(e)}")
            raise
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при обновлении цены: {str(e)}")
            raise PriceUpdateError(f"Ошибка при обновлении цены товара {product_id}")