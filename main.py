import asyncio

from core.config.database import DataBaseConnection
from core.logger import logger
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from infrastructure.parsers.browser import BrowserManager
from infrastructure.parsers.parser import ProductParser
from domain.entities.product_fields import ProductFields
from application.collector import Collector
from application.use_cases.check_price import CheckPriceUseCase


async def run():
    database = DataBaseConnection()
    uow_factory = UnitOfWorkFactory(database)
    collector = Collector(uow_factory)
    update_prices = CheckPriceUseCase(uow_factory)

    async with BrowserManager(headless=True) as browser:
        parser = ProductParser(browser=browser, fields=ProductFields())

        # 1. Собираем данные из БД: {user_id: [product_ids]}
        raw_data = await collector.pick_up()
        logger.info(f'Собрано {len(raw_data)} групп пользователей')

        # 2. Преобразуем ID → URL: {chat_id: [urls]}
        vectorized = await collector.to_vectorize(raw_data)
        logger.info(f'Получено {len(vectorized)} chat_id для парсинга')

        # 3. Упаковываем в UserProductsData
        tasks = await collector.form_groups(vectorized)
        logger.info(f'Сформировано {len(tasks)} задач на парсинг')

        # 4. Парсим страницы и обновляем цены
        all_changes = []
        for task in tasks:
            parsed = await parser.parse(task)
            changes = await update_prices.execute(parsed)
            all_changes.extend(changes)

        # 5. Итог
        if all_changes:
            logger.info(f'Обнаружено {len(all_changes)} изменений цен')
            for change in all_changes:
                logger.info(
                    f'  {change["name"]}: '
                    f'{change["old_price"]} -> {change["new_price"]}'
                )
        else:
            logger.info('Изменений цен не обнаружено')

    await uow_factory.close()


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
