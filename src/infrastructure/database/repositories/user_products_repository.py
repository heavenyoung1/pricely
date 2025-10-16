import logging
from collections import defaultdict

from src.application.interfaces.repositories import UserProductsRepository
from src.infrastructure.database.mappers import UserMapper
from src.infrastructure.database.models import ORMUserProducts

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class UserProductsRepositoryImpl(UserProductsRepository):
    '''Реализация репозитория для работы с товарами пользователя в базе данных.'''

    def __init__(self, session: Session):
        '''
        Инициализация репозитория для работы с товарами пользователя.

        :param session: Экземпляр SQLAlchemy Session для работы с базой данных.
        '''
        self.session = session

    def get_products_for_user(self, user_id: str) -> list:
        '''
        Получить список продуктов для конкретного пользователя.

        :param user_id: Идентификатор пользователя.
        :return: Список идентификаторов продуктов пользователя.
        '''
        logger.debug(f'Получение списка продуктов для пользователя {user_id}')
        rows = (
            self.session.query(ORMUserProducts)
            .filter(ORMUserProducts.user_id == user_id)
            .all()
        )
        product_ids = [row.product_id for row in rows]
        logger.debug(f'Продукты пользователя {user_id}: {product_ids}')
        return product_ids

    def add_product_for_user(self, user_id: str, product_id: str) -> None:
        '''
        Создает запись в таблице user_products (связка user_id и product_id).

        :param user_id: Идентификатор пользователя.
        :param product_id: Идентификатор продукта.
        '''
        logger.info(f'Привязка товара ID {product_id} пользователю ID {user_id}')
        record = ORMUserProducts(user_id=user_id, product_id=product_id)
        self.session.add(record)

    def get_all_user_products_pair(self) -> list:
        '''
        Получить все пары (product_id, user_id) из таблицы user_products.

        :return: Список словарей с полями 'product_id' и 'user_id'.
        '''
        #logger.debug('Извлекаем данные {product_id:user_id} из репозитория UserProductsRepositoryImpl')
        rows = self.session.query(ORMUserProducts).all()
        records = [{'product_id': row.product_id, 'user_id': row.user_id} for row in rows]
        #logger.debug('Записи список(словарей) получен и готов для парсинга.')
        return records

    def get_sorted_user_products(self) -> dict:
        '''
        Извлекает все товары и пользователей, группируя товары по user_id.

        Возвращает словарь вида: {user_id: [product_id, product_id, ...], ...}

        :return: Словарь с user_id как ключом и списком product_id как значениями.
        '''
        logger.info('Извлекаем данные {product_id:user_id} из репозитория UserProductsRepositoryImpl')

        # Запрос всех строк из базы
        rows = self.session.query(ORMUserProducts).all()

        # Используем defaultdict для автоматического создания списка для каждого user_id
        logger.info(f'Rows -> {rows}')
        user_products = defaultdict(list)

        for row in rows:
            # logger.debug(f'user_products Iteration -> {user_products}')
            user_products[row.user_id].append(row.product_id)

        #logger.info(f'Записи список (user_id: [product_id, product_id, ...]) получен и готов для парсинга.')
        return dict(user_products)  # Преобразуем defaultdict обратно в обычный dict