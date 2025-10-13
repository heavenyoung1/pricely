from src.application.interfaces.repositories import UserProductsRepository
import logging

logger = logging.getLogger(__name__)

class LinkUserProductUseCase:
    '''
    Use case для создания связи между пользователем и продуктом.

    Этот класс отвечает за добавление связи между пользователем и продуктом в базе данных,
    если такой связи ещё не существует.
    '''

    def __init__(self, user_products_repo: UserProductsRepository):
        '''
        Инициализация UseCase для создания связи между пользователем и продуктом.

        :param user_products_repo: Репозиторий для работы с привязками пользователей и товаров.
        '''
        self.user_products_repo = user_products_repo

    def execute(self, user_id: str, product_id: str):
        '''
        Создаёт связь между пользователем и продуктом.

        1. Проверяет, существует ли уже связь между пользователем и продуктом.
        2. Если связь существует, логирует это и пропускает дальнейшие действия.
        3. Если связь не существует, создаёт её.

        :param user_id: Идентификатор пользователя.
        :param product_id: Идентификатор продукта.
        '''
        # 1. Проверяем, существует ли уже связь между пользователем и продуктом
        existing = self.user_products_repo.get_products_for_user(user_id)
        if product_id in [row['product_id'] for row in existing]:  # Исправлена ошибка синтаксиса
            logger.info(f'Продукт {product_id} уже связан с пользователем {user_id}')
            return

        # 2. Создаем связь, если ее нет
        self.user_products_repo.add_product_for_user(user_id, product_id)
        logger.info(f'Успешно связали пользователя {user_id} с продуктом {product_id}')
