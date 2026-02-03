import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config.settings import settings
from core.config.database import DataBaseConnection
from core.logger import logger
from infrastructure.database.unit_of_work import UnitOfWorkFactory
from presentation.telegram.handlers import setup_routers


async def on_startup(bot: Bot):
    logger.info('Бот запущен')


async def on_shutdown(bot: Bot):
    logger.info('Бот остановлен')


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

    # Запуск
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
