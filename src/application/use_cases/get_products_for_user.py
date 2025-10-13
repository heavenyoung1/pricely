from src.application.interfaces.repositories import ProductRepository, PriceRepository, UserProductsRepository
import logging
from typing import List

logger = logging.getLogger(__name__)

class GetProductForUserUseCase:
    '''
    Use case для получения списка товаров пользователя.

    Этот класс отвечает за извлечение списка идентификаторов товаров, 
    привязанных к пользователю, из базы данных.
    '''

    def __init__(
        self,
        user_products_repo: UserProductsRepository,
        product_repo: ProductRepository,
        price_repo: PriceRepository,
    ):
        '''
        Инициализация UseCase для получения товаров пользователя.

        :param user_products_repo: Репозиторий для работы с привязками товаров и пользователей.
        :param product_repo: Репозиторий для работы с продуктами.
        :param price_repo: Репозиторий для работы с ценами.
        '''
        self.user_products_repo = user_products_repo
        self.product_repo = product_repo
        self.price_repo = price_repo

    def execute(self, user_id: str) -> List[str]:
        '''
        Основной метод для получения списка товаров пользователя.

        1. Извлекает список идентификаторов товаров для указанного пользователя.
        2. Преобразует идентификаторы товаров в строковый формат.
        3. Возвращает список идентификаторов товаров.

        :param user_id: Идентификатор пользователя.
        :return: Список строковых идентификаторов товаров, привязанных к пользователю.
        '''
        logger.info(f'Запрос списка товаров для пользователя ID: {user_id}')
        
        # 1. Получаем сырые данные о товарах пользователя
        raw_ids = self.user_products_repo.get_products_for_user(user_id)
        if not raw_ids:
            logger.info(f'Для пользователя {user_id} не найдено товаров')
            return []
        
        # 2. Преобразуем идентификаторы товаров в строки
        ids = [str(x) for x in raw_ids]
        logger.debug(f'Идентификаторы товаров пользователя {user_id}: {ids}')
        
        # 3. Возвращаем список идентификаторов
        return ids