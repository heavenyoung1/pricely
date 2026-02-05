'''
Точка входа для сервиса проверки цен.

Запускает CheckerService с планировщиком, который периодически
проверяет цены товаров и публикует уведомления в Redis.

Запуск:
    python -m checker_main

Или через Docker:
    docker-compose up checker
'''

import asyncio
import signal

from infrastructure.parsers.proxy import ProxyController
from core.config.database import DataBaseConnection
from core.config.settings import settings
from core.logger import logger
from domain.entities.product_fields import ProductFieldsForAdd, ProductFieldsForCheck
from domain.services.checker_service import CheckerService
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from infrastructure.parsers.browser import BrowserManager
from infrastructure.parsers.parser import ProductParser
from infrastructure.redis.publisher import NotificationPublisher


async def main():
    logger.info('Запуск сервиса проверки цен...')

    # Инициализация компонентов
    database = DataBaseConnection()
    uow_factory = UnitOfWorkFactory(database)
    publisher = NotificationPublisher()

    await publisher.connect()

    # Флаг для graceful shutdown
    shutdown_event = asyncio.Event()

    def signal_handler():
        logger.info('Получен сигнал завершения')
        shutdown_event.set()

    # Регистрация обработчиков сигналов
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, signal_handler)
        except NotImplementedError:
            # Windows не поддерживает add_signal_handler
            pass

    # Получаем прокси если включено
    proxy_controller = ProxyController()
    proxy = proxy_controller.get_proxy_if_enabled(settings.USE_PROXY)
    logger.info(f'[MAIN] Прокси для браузера: {proxy}')

    try:
        async with BrowserManager(
            proxy=proxy,
            delay=settings.DELAY,
            
            ) as browser:
            parser = ProductParser(
                browser=browser,
                fields_for_add=ProductFieldsForAdd(),
                fields_for_check=ProductFieldsForCheck(),
            )

            checker = CheckerService(
                uow_factory=uow_factory,
                parser=parser,
                publisher=publisher,
            )

            # Запускаем планировщик
            checker.start(cron=settings.CHECKER_CRON)

            logger.info(f'Сервис запущен. Расписание: {settings.CHECKER_CRON}')
            logger.info('Для остановки нажмите Ctrl+C')

            # Запускаем первую проверку сразу при старте
            await checker.run_check()

            # Ожидаем сигнал завершения
            await shutdown_event.wait()

            # Graceful shutdown
            checker.stop()

    finally:
        await publisher.close()
        await uow_factory.close()
        logger.info('Сервис проверки цен остановлен')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Прервано пользователем')
