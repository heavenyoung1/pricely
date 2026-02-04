from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from application.collector import Collector
from application.use_cases.check_price import CheckPriceUseCase
from application.use_cases.create_notify import CreateNotifyUseCase
from domain.entities.notification import Notification
from infrastructure.parsers.parser import ProductParser
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from infrastructure.redis.publisher import NotificationPublisher
from infrastructure.redis.message import NotificationMessage
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

            # 3. Получаем связи user-product для изменившихся товаров
            product_ids = [price.product_id for price in changed_prices]
            async with self.uow_factory.create() as uow:
                user_links = await uow.user_products_repo.get_users_by_product_ids(
                    product_ids
                )

            # 4. Формируем уведомления
            notify_use_case = CreateNotifyUseCase()
            notifications = await notify_use_case.execute(changed_prices, user_links)

            # 5. Конвертируем в Redis сообщения и публикуем
            messages = await self._build_messages(notifications)
            published_count = await self.publisher.publish_many(messages)

            logger.info(
                f'Проверка завершена. Опубликовано {published_count} уведомлений'
            )

        except Exception as e:
            logger.error(f'Ошибка при проверке цен: {e}')

    async def _build_messages(
        self, notifications: List[Notification]
    ) -> List[NotificationMessage]:
        '''
        Собирает полные данные для уведомлений.

        Обогащает уведомления данными из БД (chat_id, product info),
        чтобы бот мог отправить сообщение без обращения к БД.
        '''
        messages = []

        async with self.uow_factory.create() as uow:
            for notify in notifications:
                # Получаем chat_id пользователя
                user = await uow.user_repo.get(notify.user_id)
                if not user:
                    logger.warning(f'Пользователь {notify.user_id} не найден')
                    continue

                # Получаем информацию о товаре
                product = await uow.product_repo.get(notify.price.product_id)
                if not product:
                    logger.warning(f'Товар {notify.price.product_id} не найден')
                    continue

                message = NotificationMessage(
                    chat_id=user.chat_id,
                    product_name=product.name,
                    product_link=product.link,
                    price_with_card=notify.price.with_card,
                    price_without_card=notify.price.without_card,
                    previous_with_card=notify.price.previous_with_card,
                    previous_without_card=notify.price.previous_without_card,
                )
                messages.append(message)

        return messages

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
