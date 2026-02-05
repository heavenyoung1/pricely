from typing import List, Dict

from domain.entities.user_products import UserProductsData
from domain.entities.price import Price

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
                data_urls = [await uow.product_repo.get_link(id) for id in data_ids]
                return data_urls

            except Exception as e:
                logger.error(f'Ошибка при получении всех товаров: {e}')
                raise

    # async def collect_data_for_send_notifications(
    #         self, 
    #         changed_prices: List['Price'],
    #         ) -> List['NewNotification']:
    #     product_ids = [price.product_id for price in changed_prices]
    #     async with self.uow_factory.create() as uow:
    #         data_records = await uow.general_repo.get_records_by_changed_prices(product_ids)
    #     logger.debug(f'[DATA_RECORDS] {data_records}')
    #     grouped_data = {}
    #     for record in data_records:
    #         if not grouped_data.get(record.chat_id):
    #             grouped_data[record.chat_id] = [].append(record)
    #         else:
    #             key, value = grouped_data.items()
    #             value.append(record)
        
    #     logger.debug(f'[GROUPED_DATA] {grouped_data}')

