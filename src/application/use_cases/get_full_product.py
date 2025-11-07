import logging
from src.application.interfaces.repositories import (
    ProductRepository,
    PriceRepository,
    UserRepository,
)
from src.domain.exceptions import ProductNotFoundError

logger = logging.getLogger(__name__)


class GetFullProductUseCase:
    """
    Use case для получения полного продукта с его последней ценой.

    Этот класс отвечает за извлечение данных о продукте и его последней цене из системы.
    """

    def __init__(
        self,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
        user_repo: UserRepository,
    ):
        """
        Инициализация UseCase для получения полного продукта.

        :param product_repo: Репозиторий для работы с продуктами.
        :param price_repo: Репозиторий для работы с ценами.
        :param user_repo: Репозиторий для работы с пользователями.
        """
        self.product_repo = product_repo
        self.price_repo = price_repo
        self.user_repo = user_repo

    def execute(self, product_id: str) -> dict:
        """
        Основной метод для выполнения логики получения полного продукта.

        1. Проверяет наличие продукта в базе данных.
        2. Извлекает информацию о продукте.
        3. Получает последнюю цену для продукта.
        4. Возвращает полные данные о продукте.

        :param product_id: Идентификатор продукта.
        :return: Словарь с полными данными о продукте и его последней цене.
        :raises ProductNotFoundError: Если продукт с данным ID не найден.
        """
        # 1. Получаем продукт из репозитория
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning(f"Продукт {product_id} не найден")
            raise ProductNotFoundError(f"Продукт {product_id} не найден")

        # 2. Получаем последнюю цену для продукта
        latest_price = self.price_repo.get_latest_for_product(product_id)

        # 3. Формируем последние цены (с картой и без)
        latest = {
            "with_card": latest_price.with_card if latest_price else None,
            "without_card": latest_price.without_card if latest_price else None,
            "previous_price_with_card": (
                latest_price.previous_with_card if latest_price else None
            ),
            "previous_price_without_card": (
                latest_price.previous_without_card if latest_price else None
            ),
        }

        # 4. Возвращаем полный набор данных о продукте и его последней цене
        return {
            "id": product.id,
            "name": product.name,
            "link": product.link,
            "latest_price": latest,
            "created_at": latest_price.created_at if latest_price else None,
        }
