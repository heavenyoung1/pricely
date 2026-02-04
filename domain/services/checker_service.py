from typing import TYPE_CHECKING

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from application.collector import Collector
from application.use_cases.check_price import CheckPriceUseCase
from application.use_cases.create_notify import CreateNotifyUseCase
from infrastructure.parsers.parser import ProductParser
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from core.logger import logger

if TYPE_CHECKING:
    from infrastructure.services.telegram_sender import TelegramNotificationSender


class CheckerService:
    '''
    Сервис периодической проверки цен товаров.

    Отвечает за:
    - Запуск проверки цен по расписанию
    - Сбор URL товаров для парсинга
    - Проверку изменений цен
    - Координацию отправки уведомлений
    '''

    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        parser: ProductParser,
        notification_sender: 'TelegramNotificationSender',
    ):
        self.uow_factory = uow_factory
        self.parser = parser
        self.notification_sender = notification_sender
        self.scheduler = AsyncIOScheduler()

    async def run_check(self) -> None:
        '''
        Выполняет полный цикл проверки цен.

        1. Собирает URL всех отслеживаемых товаров
        2. Парсит текущие цены
        3. Сравнивает с БД и сохраняет изменения
        4. Формирует и отправляет уведомления
        '''
        logger.info('Запуск проверки цен...')

        try:
            # 1. Собираем URL для парсинга
            collector = Collector(self.uow_factory)
            urls = await collector.collect_data_for_parsing()

            if not urls:
                logger.info('Нет товаров для проверки')
                return

            logger.info(f'Найдено {len(urls)} товаров для проверки')

            # 2. Проверяем цены и получаем изменившиеся
            check_use_case = CheckPriceUseCase(self.parser, self.uow_factory)
            changed_prices = await check_use_case.execute(urls)

            if not changed_prices:
                logger.info('Изменений цен не обнаружено')
                return

            logger.info(f'Обнаружено {len(changed_prices)} изменений цен')

            # 3. Получаем связи user-product для изменившихся товаров
            product_ids = [price.product_id for price in changed_prices]
            async with self.uow_factory.create() as uow:
                user_links = await uow.user_products_repo.get_users_by_product_ids(
                    product_ids
                )

            # 4. Формируем уведомления
            notify_use_case = CreateNotifyUseCase()
            notifications = await notify_use_case.execute(changed_prices, user_links)

            # 5. Отправляем уведомления
            sent_count = await self.notification_sender.send(notifications)

            logger.info(f'Проверка завершена. Отправлено {sent_count} уведомлений')

        except Exception as e:
            logger.error(f'Ошибка при проверке цен: {e}')

    def start(self, cron: str = '0 */4 * * *') -> None:
        '''
        Запускает планировщик проверки цен.

        Args:
            cron: Cron-выражение для расписания. По умолчанию каждые 4 часа.
                  Примеры:
                  - '0 */4 * * *' — каждые 4 часа
                  - '0 9,13,18,22 * * *' — в 9, 13, 18, 22 часа
                  - '0 10 * * *' — раз в день в 10:00
        '''
        self.scheduler.add_job(
            self.run_check,
            CronTrigger.from_crontab(cron),
            id='price_checker',
            replace_existing=True,
        )
        self.scheduler.start()
        logger.info(f'Планировщик запущен с расписанием: {cron}')

    def stop(self) -> None:
        '''Останавливает планировщик.'''
        self.scheduler.shutdown()
        logger.info('Планировщик остановлен')
