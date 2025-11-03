import logging

from src.application.interfaces.repositories import ProductRepository
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError

logger = logging.getLogger(__name__)


class GetProductUseCase:
    """
    Use case для получения продукта.

    Этот класс отвечает за получение информации о продукте по его ID.
    Если продукт не найден, выбрасывает исключение.
    """

    def __init__(self, product_repo: ProductRepository):
        """
        Инициализация UseCase для получения продукта.

        :param product_repo: Репозиторий для работы с продуктами.
        """
        self.product_repo = product_repo

    def execute(self, product_id: str) -> Product:
        """
        Основной метод для выполнения логики получения продукта.

        1. Проверяет, указан ли идентификатор продукта.
        2. Извлекает информацию о продукте из репозитория.
        3. Если продукт не найден, выбрасывает исключение.

        :param product_id: Идентификатор продукта, который нужно получить.
        :return: Объект Product с данными о продукте.
        :raises ProductNotFoundError: Если продукт с данным ID не найден.
        """
        # 1. Проверяем, указан ли идентификатор продукта
        if not product_id:
            logger.error("Идентификатор продукта не указан")
            raise ProductNotFoundError("Идентификатор продукта не указан")

        # 2. Получаем продукт из репозитория
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning(f"Продукт {product_id} не найден")
            raise ProductNotFoundError(f"Продукт {product_id} не существует")

        # 3. Продукт найден, логируем успех
        logger.info(f"Продукт {product_id} успешно получен")
        return product
