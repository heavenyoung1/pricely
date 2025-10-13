from src.application.interfaces.repositories import UserProductsRepository
import logging

logger = logging.getLogger(__name__)

class GetUserProductsUseCase:
    '''
    Use case для получения всех записей user_id и product_id.

    Этот класс отвечает за извлечение всех записей связывающих пользователей и товары.
    Он может возвращать все пары товаров и пользователей, либо сортировать их.
    '''

    def __init__(self, user_products_repo: UserProductsRepository):
        '''
        Инициализация UseCase для получения продуктов пользователя.

        :param user_products_repo: Репозиторий для работы с таблицей связывания пользователей и товаров.
        '''
        self.user_products_repo = user_products_repo

    def execute(self) -> dict:
        '''
        Основной метод для выполнения логики получения всех товаров пользователей.

        1. Запрашивает данные у репозитория.
        2. Возвращает отсортированные данные всех товаров и пользователей.

        :return: Словарь с данными о пользователях и привязанных товарах.
        '''
        logger.info(f'Запрашиваем данные для запуска APSchedulerService')

        # Возвращаем отсортированные данные о всех пользователях и товарах
        return self.user_products_repo.get_sorted_user_products()
