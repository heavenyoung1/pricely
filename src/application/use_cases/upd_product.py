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
        try:
            # 1. Берем текущий продукт
            product = self.product_repo.get(product_id)
            if not product:
                raise ProductNotFoundError(f"Товар {product_id} не найден")

            # 2. Достаём последнюю цену
            last_price = self.price_repo.get_latest_for_product(product_id)

            # 3. Парсим новые данные
            new_data = self.parser.parse_product(product['link'])

            # 3. Сравниваем ценывара {product_id} обновлена: {new_price}")
            changed = (
                product['with_card'] != new_data['with_card'] or
                product['without_card'] != new_data['without_card'] 
            )

            # 4. Если цены изменились → сохраняем новую запись Price
            if changed == True:
                new_price = Price(
                    id=None,
                    product_id=product.id,
                    with_card=new_data['with_card'],
                    without_card=new_data['without_card'],
                    previous_with_card=product['with_card'],
                    previous_without_card=product['with_card'],
                    created_at= datetime.now(),
            )
            self.price_repo.save(price=new_price)

            logger.info(f"Цена для товара {product_id} успешно обновлена: {new_price}")

            # 5. Возвращаем словарь для UI
            return {
                "id": product.id,
                "name": product.name,
                "link": product.link,
                "with_card": new_price.with_card,
                "without_card": new_price.without_card,
                "last_price": last_price.with_card if last_price else None,
            }

        except ProductNotFoundError as e:
            logger.error(f"Ошибка при обновлении цены: {str(e)}")
            raise
        except Exception as e:
            logger.exception(f"Неизвестная ошибка при обновлении цены: {str(e)}")
            raise PriceUpdateError(f"Ошибка при обновлении цены товара {product_id}")
