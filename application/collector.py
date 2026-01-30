from typing import List, Dict

from domain.entities.user_products import UserProductsData
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from core.logger import logger

class Collector:
    def __init__(self, uow_factory: UnitOfWorkFactory):
        self.uow_factory = uow_factory

    async def pick_up(self):
        async with self.uow_factory as uow:
            try:
                data = await uow.user_product_repo.get_all_grouped()
                return data
            except Exception as e:
                logger.error(f'Ошибка при сборе данных: {e}')
                raise Exception(f'Ошибка при сборе данных: {e}')
            
    async def to_vectorize(
            self, 
            data: List[Dict[int, List[str]]]) -> None:
        '''
        Пример получаемых данных
        correct_data = [
            {1: ['Товар1', 'Товар2', 'Товар3']},
            {2: ['Товар3', 'Товар4', 'Товар5']}
        ]
        '''
        if data is None:
            raise ValueError('Данные не могут быть None')

        result = {}

        async with self.uow_factory as uow:
            for item in data:
                # Каждый item - словарь с одной парой {user_id: products}
                for user_id, products in item.items():
                    # 1. Получаем пользователя
                    user = await uow.user_repo.get(user_id)
                    if not user:
                        logger.error(f'Пользователь {user.id} не найден')
                        continue
                    
                    chat_id = user.chat_id

                    # 2. Инициализируем список URL для этого chat_id
                    if chat_id not in result:
                        result[chat_id] = []

                    # 3. Для каждого названия товара ищем URL
                    for product_id in products:
                        product = await uow.product_repo.get(product_id)

                        if not product:
                            logger.error(f'Товар не найден')
                            continue
                        
                        product_url = product.url
                        result[chat_id].append(product_url)
        return result

    async def submit(self, data: Dict[int, List[str]]) -> None:
        output_data = []
        for i in data:
            for chat_id, urls in data.items():
                row = UserProductsData(
                    chat_id=chat_id,
                    product_links=urls,
                )
                output_data.append(row)
        return output_data