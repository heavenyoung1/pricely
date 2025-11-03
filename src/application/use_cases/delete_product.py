import logging
from src.application.interfaces.repositories import (
    ProductRepository,
    PriceRepository,
    UserRepository,
)
from src.domain.exceptions import ProductNotExistingDataBase, ProductDeletingError

logger = logging.getLogger(__name__)


class DeleteProductUseCase:
    """
    Use case для удаления товара.

    Этот класс отвечает за удаление товара из системы, а также за удаление
    связанных с ним цен и обновление списка товаров пользователя, если это необходимо.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
    ):
        """
        Инициализация UseCase для удаления товара.

        :param user_repo: Репозиторий для работы с пользователями.
        :param product_repo: Репозиторий для работы с товарами.
        :param price_repo: Репозиторий для работы с ценами.
        """
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, product_id: str) -> None:
        """
        Основной метод для выполнения логики удаления товара.

        1. Проверяет наличие товара в базе данных.
        2. Если товар существует, удаляет связанные с ним цены.
        3. Удаляет товар из базы данных.
        4. Удаляет товар из списка продуктов пользователя, если он существует.

        :param product_id: Идентификатор товара, который необходимо удалить.
        :raises ProductNotExistingDataBase: Если товар не найден в базе данных.
        :raises ProductDeletingError: Если произошла ошибка при удалении товара.
        """
        # 1. Проверяем, существует ли товар в БД
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning(
                f"Товар {product_id} не существует в БД, пропускаем удаление"
            )
            raise ProductNotExistingDataBase(f"Товар {product_id} не существует в БД!")

        try:
            # 2. Удаляем все цены по product_id
            self.price_repo.delete_all_prices_for_product(product_id)
            logger.info(f"Цены для товара {product_id} удалены")

            # 3. Удаляем товар из БД
            self.product_repo.delete(product_id)
            logger.debug(f"Товар {product_id} удален")

            # 4. Удаляем товар из списка продуктов пользователя
            user = self.user_repo.get(product.user_id)
            if user and product_id in user.products:
                user.products.remove(product_id)
                self.user_repo.save(user)
                logger.debug(
                    f"Товар {product_id} удален из списка пользователя {product.user_id}"
                )

            logger.info(f"Операция удаления выполнена для ID {product_id}")

        except Exception as e:
            logger.error(f"Ошибка при удалении товара {product_id}: {str(e)}")
            raise ProductDeletingError(f"Ошибка удаления товара: {str(e)}")
