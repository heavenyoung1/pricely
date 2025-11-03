import logging
from src.application.interfaces.repositories import ProductRepository, PriceRepository
from src.domain.entities import Price
from src.domain.exceptions import ProductNotFoundError, PriceUpdateError
from src.infrastructure.parsers.ozon_parser import OzonParser
from datetime import datetime

logger = logging.getLogger(__name__)


class UpdateProductPriceUseCase:
    """
    Use case для обновления цены товара.

    Этот класс отвечает за обновление цены товара:
    - извлечение текущих данных о продукте,
    - получение последней цены из базы данных,
    - парсинг новых данных о цене,
    - сохранение обновленной цены в базе данных.
    """

    def __init__(
        self,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        parser: OzonParser,
    ):
        """
        Инициализация UseCase для обновления цены товара.

        :param product_repo: Репозиторий для работы с продуктами.
        :param price_repo: Репозиторий для работы с ценами.
        :param parser: Парсер для получения данных о товаре с внешнего ресурса.
        """
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.parser = parser

    def execute(self, product_id: str) -> dict:
        """
        Основной метод для выполнения логики обновления цены товара.

        1. Извлекает информацию о товаре по его ID.
        2. Получает текущую цену товара.
        3. Парсит новые данные о цене.
        4. Сравнивает старую цену с новой.
        5. Если цена изменилась, сохраняет обновленную цену в БД.

        :param product_id: Идентификатор товара, для которого обновляется цена.
        :return: Словарь с информацией о цене и флагом изменения.
        :raises ProductNotFoundError: Если продукт не найден в базе данных.
        :raises PriceUpdateError: Если произошла ошибка при обновлении цены.
        """
        # Флаг, указывающий, изменилась ли цена
        is_changed: bool = False

        try:
            # 1. Получаем текущий продукт из репозитория
            product = self.product_repo.get(product_id)
            if not product:
                raise ProductNotFoundError(f"Товар {product_id} не найден")

            # 2. Достаём актуальную цену из БД
            last_price = self.price_repo.get_latest_for_product(product_id)

            previous_price_with_card = last_price.with_card if last_price else None
            previous_price_without_card = (
                last_price.without_card if last_price else None
            )

            # 3. ПРОВЕРЯЕМ новые данные о товаре с помощью парсера, используется другой метод
            try:
                parsed_check_price = self.parser.check_product(product.link)
            except Exception as e:
                logger.error(f"Ошибка при парсинге данных для товара {product_id}: {e}")
                raise PriceUpdateError(
                    f"Ошибка при парсинге данных для товара {product_id}"
                )

            actual_price_with_card = parsed_check_price["price_with_card"]
            actual_price_without_card = parsed_check_price["price_without_card"]

            # 4. Создаём новую сущность цены
            price = Price(
                id=None,  # Автоинкрементируемый ID
                product_id=product.id,
                with_card=actual_price_with_card,
                without_card=actual_price_without_card,
                previous_with_card=previous_price_with_card,
                previous_without_card=previous_price_without_card,
                created_at=datetime.now(),
            )

            # 5. Проверяем, изменилась ли цена, и если да, сохраняем её в БД
            if actual_price_with_card != previous_price_with_card:
                is_changed = True
                try:
                    self.price_repo.save(price)
                except Exception as e:
                    logger.error(f"Ошибка обновления цены товара {product_id}: {e}")
                    raise PriceUpdateError(
                        f"Ошибка обновления цены товара {product_id}"
                    )

            # 6. Возвращаем данные о товаре и цене
            data_return = {
                "is_changed": is_changed,  # Флаг изменения цены
                "product_data": {
                    "id": product.id,
                    "name": product.name,
                    "link": product.link,
                    "with_card": actual_price_with_card,
                    "without_card": actual_price_without_card,
                    "previous_price_with_card": previous_price_with_card,
                    "previous_price_without_card": previous_price_without_card,
                },
            }

            # Логирование результатов
            logger.info(
                f"Предыдущая цена с картой: {previous_price_with_card}, новая цена с картой: {actual_price_with_card}"
            )
            logger.info(
                f"Данные, возвращаемые UpdateProductPriceUseCase: {data_return}"
            )

            return data_return

        except ProductNotFoundError as e:
            logger.error(f"Ошибка при обновлении цены: {str(e)}")
            raise
        except Exception as e:
            logger.exception(
                f"Неизвестная ошибка при обновлении цены товара {product_id}: {str(e)}"
            )
            raise PriceUpdateError(f"Ошибка при обновлении цены товара {product_id}")
