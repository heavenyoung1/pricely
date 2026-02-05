from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from application.collector import Collector
from application.use_cases.check_price import CheckPriceUseCase
from infrastructure.parsers.parser import ProductParser
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from infrastructure.redis.publisher import NotificationPublisher
from infrastructure.redis.message import NotificationMessage, PriceChangeItem
from core.logger import logger


class CheckerService:
    '''
    Сервис периодической проверки цен товаров.

    Отвечает за:
    - Запуск проверки цен по расписанию
    - Сбор URL товаров для парсинга
    - Проверку изменений цен
    - Публикацию уведомлений в Redis очередь
    '''

    def __init__(
        self,
        uow_factory: UnitOfWorkFactory,
        parser: ProductParser,
        publisher: NotificationPublisher,
    ):
        self.uow_factory = uow_factory
        self.parser = parser
        self.publisher = publisher
        self.scheduler = AsyncIOScheduler()

    async def run_check(self) -> None:
        '''
        Выполняет полный цикл проверки цен.

        1. Собирает URL всех отслеживаемых товаров
        2. Парсит текущие цены
        3. Сравнивает с БД и сохраняет изменения
        4. Формирует и публикует уведомления в Redis
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

            grouped_data = await collector.collect_data_for_send_notifications(
                changed_prices
            )

            # 3. Конвертируем сгруппированные данные в Redis-сообщения и публикуем
            messages = []
            for chat_id, records in grouped_data.items():
                items = [
                    PriceChangeItem(
                        product_name=r['name'],
                        product_link=r['product_link'],
                        price_with_card=r['product_with_card'],
                        price_without_card=r['product_without_card'],
                        previous_with_card=r['product_previous_with_card'],
                        previous_without_card=r['product_previous_without_card'],
                    )
                    for r in records
                ]
                messages.append(NotificationMessage(chat_id=chat_id, items=items))

            published_count = await self.publisher.publish_many(messages)
            logger.info(
                f'Проверка завершена. Опубликовано {published_count} уведомлений'
            )

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
