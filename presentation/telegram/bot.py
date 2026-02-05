import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config.settings import settings
from core.config.database import DataBaseConnection
from core.logger import logger
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from infrastructure.redis.subscriber import NotificationSubscriber
from presentation.telegram.handlers import setup_routers
from domain.services.notify_service import NotificationHandler


async def on_startup(bot: Bot):
    logger.info('Бот запущен')


async def on_shutdown(bot: Bot):
    logger.info('Бот остановлен')


async def run_notification_listener(bot: Bot, subscriber: NotificationSubscriber):
    '''Запускает слушателя уведомлений из Redis'''
    handler = NotificationHandler(bot)
    await subscriber.connect()
    logger.info('Запущен слушатель уведомлений')

    try:
        await subscriber.listen(handler.handle)
    except asyncio.CancelledError:
        logger.info('Слушатель уведомлений остановлен')
    finally:
        await subscriber.close()


async def main():
    # Инициализация БД
    database = DataBaseConnection()
    uow_factory = UnitOfWorkFactory(database)

    # Инициализация бота
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp['uow_factory'] = uow_factory

    # Регистрация роутеров
    dp.include_router(setup_routers())

    # Регистрация событий
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Инициализация слушателя Redis
    subscriber = NotificationSubscriber()

    # Запуск
    try:
        # Запускаем polling и слушателя параллельно
        await asyncio.gather(
            dp.start_polling(bot),
            run_notification_listener(bot, subscriber),
        )
    finally:
        subscriber.stop()
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
