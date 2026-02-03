from typing import List, Dict

from domain.entities.user_products import UserProductsData
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from core.logger import logger

class Collector:
    '''
    Сборщик данных для подготовки информации о товарах пользователей.

    Отвечает за:
    - Извлечение связей пользователь-товары из базы данных
    - Преобразование идентификаторов в URL товаров
    - Формирование итоговой структуры для дальнейшей обработки
    '''

    def __init__(self, uow_factory: UnitOfWorkFactory):
        '''
        Инициализация коллектора.

        Args:
            uow_factory: Фабрика для создания Unit of Work,
                         обеспечивает доступ к репозиториям БД.
        '''
        self.uow_factory = uow_factory

    async def pick_up(self) -> List[Dict[int, List[int]]]:
        '''
        Извлекает сгруппированные данные о товарах пользователей из БД.

        Returns:
            Список словарей, где ключ — user_id, значение — список product_id.
            Пример: [{18631204: [1, 2, 3]}, {72305231: [3, 4, 5]}]

        Raises:
            Exception: При ошибке обращения к базе данных.
        '''
        async with self.uow_factory.create() as uow:
            try:
                data = await uow.user_products_repo.get_all_grouped()
                return data
            except Exception as e:
                logger.error(f'Ошибка при сборе данных: {e}')
                raise

    async def collect_data_for_parsing(self) -> list[str]:
        '''
        Собирает URL всех отслеживаемых товаров для парсинга.

        Получает из БД идентификаторы всех товаров пользователей,
        затем преобразует их в URL для последующего парсинга цен.

        Returns:
            Список URL товаров для парсинга.
            Пример: ['https://shop.com/item1', 'https://shop.com/item2']

        Raises:
            Exception: При ошибке обращения к базе данных.
        '''
        async with self.uow_factory.create() as uow:
            try:
                data_ids = await uow.user_products_repo.get_all_product_ids()
                data_urls = [
                    await uow.product_repo.get_link(id) for id in data_ids
                    ]
                return data_urls

            except Exception as e:
                logger.error(f'Ошибка при получении всех товаров: {e}')
                raise


    async def to_vectorize(
            self,
            data: List[Dict[int, List[int]]]) -> Dict[int, List[str]]:
        '''
        Преобразует данные: заменяет user_id на chat_id, product_id на URL.

        Для каждого пользователя получает его chat_id из БД,
        для каждого товара — его URL. Группирует URL по chat_id.

        Args:
            data: Список словарей {user_id: [product_id, ...]}.
                  Пример входных данных:
                  [
                      {18631204: [1, 2, 3]},
                      {72305231: [3, 4, 5]}
                  ]

        Returns:
            Словарь {chat_id: [url, ...]}.
            Пример: {123456789: ['https://...', 'https://...']}

        Raises:
            ValueError: Если data равен None.
        '''
        if data is None:
            raise ValueError('Данные не могут быть None')

        result = {}

        async with self.uow_factory.create() as uow:
            for item in data:
                # Каждый item - словарь с одной парой {user_id: products}
                for user_id, products in item.items():
                    # 1. Получаем пользователя
                    user = await uow.user_repo.get(user_id)
                    if not user:
                        logger.error(f'Пользователь {user_id} не найден')
                        continue

                    chat_id = user.chat_id

                    # 2. Инициализируем список URL для этого chat_id
                    if chat_id not in result:
                        result[chat_id] = []

                    # 3. Для каждого названия товара ищем URL
                    for product_id in products:
                        product = await uow.product_repo.get(product_id)

                        if not product:
                            logger.error(f'Товар {product_id} не найден')
                            continue

                        product_url = product.url
                        result[chat_id].append(product_url)
        return result

    async def form_groups(self, data: Dict[int, List[str]]) -> List[UserProductsData]:
        '''
        Формирует итоговый список объектов UserProductsData.

        Преобразует словарь {chat_id: [url, ...]} в список объектов,
        готовых для дальнейшей обработки (например, отправки уведомлений).

        Args:
            data: Словарь {chat_id: [url, ...]}, результат работы to_vectorize().
                  Пример: {123456789: ['https://...', 'https://...']}

        Returns:
            Список объектов UserProductsData, каждый содержит chat_id
            и список ссылок на товары этого пользователя.
        '''
        output_data = []
        for chat_id, urls in data.items():
            row = UserProductsData(
                chat_id=chat_id,
                product_links=urls,
            )
            output_data.append(row)
        return output_data

