import asyncio
from src.infrastructure.services.scheduler_service import APSchedulerService
from src.infrastructure.services import ProductService, NotificationService, ServiceMiddleware
from src.core import SQLAlchemyUnitOfWork
from src.presentation.bot.bot import create_bot, register_message_handlers, register_callback_handlers, register_fallback_handler
from src.infrastructure.services.logger import logger

async def main() -> None:
    bot, dp = await create_bot()
    logger.info('Бот запущен')

    # ===== СОЗДАЁМ СЕРВИСЫ =====
    product_service = ProductService(uow_factory=SQLAlchemyUnitOfWork)
    notification_service = NotificationService(bot)

    # ===== РЕГИСТРИРУЕМ MIDDLEWARE =====
    # Middleware должен быть зарегистрирован ДО регистрации обработчиков
    dp.message.middleware(ServiceMiddleware(
        product_service=product_service,
        notification_service=notification_service
    ))
    dp.callback_query.middleware(ServiceMiddleware(
        product_service=product_service,
        notification_service=notification_service
    ))

    # ===== РЕГИСТРАЦИЯ ОБРАБОТЧИКОВ =====
    register_message_handlers(dp)
    register_callback_handlers(dp)
    register_fallback_handler(dp)

    # ===== ЗАПУСК ПЛАНИРОВЩИКА =====
    scheduler = APSchedulerService(
        bot=bot,
        product_service=product_service,
        notification_service=notification_service,
        interval_minutes=120  # интервал обновления
    )
    scheduler.start()
    logger.info('✅ Планировщик успешно запущен!')

    # ===== СТАРТ БОТА =====
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
