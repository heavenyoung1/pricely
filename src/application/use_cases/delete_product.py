import logging
from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserRepository
from src.domain.exceptions import ProductNotExistingDataBase, ProductDeletingError

logger = logging.getLogger(__name__)


class DeleteProductUseCase:
    def __init__(
            self, 
            user_repo: UserRepository,
            product_repo: ProductRepository, 
            price_repo: PriceRepository
            ):
        self.user_repo = user_repo
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, product_id: str) -> None:
        product = self.product_repo.get(product_id)
        if not product:
            logger.warning(f'Товар {product_id} не существует в БД, пропускаем удаление')
            raise ProductNotExistingDataBase(f'Товар {product_id} не существует в БД!')

        try:
             # Удаляем все цены по product_id
            prices = self.price_repo.get_all_prices_by_product(product_id)
            for price in prices:
                self.price_repo.delete(price.id)
                logger.debug(f'Цена {price.id} удалена для товара {product_id}')

            # Удаление товара
            self.product_repo.delete(product_id)
            logger.debug(f'Товар {product_id} удален')

            # Удалить связь у пользователя
            user = self.user_repo.get(product.user_id)
            if user and product_id in user.products:
                user.products.remove(product_id)
                self.user_repo.save(user)
                logger.debug(f'Товар {product_id} удален из списка пользователя {product.user_id}')

            logger.info(f'Операция удаления выполнена для ID {product_id}')

        except Exception as e:
            logger.error(f'Ошибка при удалении товара {product_id}: {str(e)}')
            raise ProductDeletingError(f'Ошибка удаления товара: {str(e)}')