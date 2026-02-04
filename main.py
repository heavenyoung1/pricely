import asyncio

from core.config.database import DataBaseConnection
from core.logger import logger
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from infrastructure.parsers.browser import BrowserManager
from infrastructure.parsers.parser import ProductParser
from domain.entities.product_fields import ProductFieldsForAdd, ProductFieldsForCheck
from application.collector import Collector
from application.use_cases.check_price import CheckPriceUseCase


async def run():
    database = DataBaseConnection()
    uow_factory = UnitOfWorkFactory(database)
    collector = Collector(uow_factory)

    async with BrowserManager() as browser:
        parser = ProductParser(
            browser=browser,
            fields_for_add=ProductFieldsForAdd(),
            fields_for_check=ProductFieldsForCheck(),
        )

        # 1. Собираем URL всех товаров для проверки
        urls = await collector.collect_data_for_parsing()

        if not urls:
            logger.info('Нет товаров для проверки')
            await uow_factory.close()
            return

        logger.info(f'Найдено {len(urls)} товаров для проверки')

        # 2. Проверяем цены и получаем изменившиеся
        check_price_use_case = CheckPriceUseCase(parser, uow_factory)
        changed_prices = await check_price_use_case.execute(urls)

        # 3. Итог
        if changed_prices:
            logger.info(f'Обнаружено {len(changed_prices)} изменений цен')
            for price in changed_prices:
                logger.info(
                    f'  Товар #{price.product_id}: '
                    f'{price.previous_with_card} -> {price.with_card}'
                )
        else:
            logger.info('Изменений цен не обнаружено')

    await uow_factory.close()


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
