from src.infrastructure.services import product_service, NotificationService
from src.infrastructure.services.logger import logger
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard
from src.presentation.bot.handlers.products import _build_price_update_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
import asyncio


class APSchedulerService:
    def __init__(self, bot, product_service, notification_service, interval_minutes=1):
        """
        Сервис планировщика (APS).
        Запускает обновление товаров и уведомления при изменении цен.
        """
        self.scheduler = BackgroundScheduler()
        self.bot = bot
        self.product_service = product_service
        self.notification_service = notification_service
        self.interval_minutes = interval_minutes

        # Логирование результатов задач
        self.scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def start(self):
        """Запуск планировщика."""
        self.scheduler.add_job(self.run_price_update, 'interval', minutes=self.interval_minutes, id="update_prices")
        self.scheduler.start()
        logger.info(f"🔁 APScheduler запущен (интервал: {self.interval_minutes} мин).")

    def stop(self):
        """Остановка планировщика."""
        self.scheduler.shutdown()
        logger.info("🛑 APScheduler остановлен.")

    def listener(self, event):
        """Логирование результатов выполнения задач."""
        if event.exception:
            logger.error(f"Ошибка выполнения задачи: {event.exception}")
        else:
            logger.info("✅ ShedulerService выполнил задачу успешно.")

    def run_price_update(self):
        """Фоновое задание для обновления цен."""
        logger.info("🚀 Запуск автоматического обновления цен...")

        try:
            products = self.product_service.get_all_products_for_update()
            if not products:
                logger.info("Нет товаров для обновления.")
                return

            loop = asyncio.get_event_loop()

            for product in products:
                result = asyncio.run_coroutine_threadsafe(
                    self.product_service.update_product_price(product["id"]),
                    loop
                ).result()

                # Если цена изменилась — уведомляем пользователей
                if result["is_changed"]:
                    users = self.product_service.get_users_by_product(product["full_product"]["id"])
                    for user in users:
                        chat_id = getattr(user, "chat_id", None)
                        if chat_id:
                            asyncio.run_coroutine_threadsafe(
                                self.notification_service.notify_price_change(
                                    chat_id=chat_id,
                                    updated_product=result["full_product"],
                                    full_product=result["full_product"]
                                ),
                                loop
                            )

            logger.info("✅ Автоматическое обновление цен завершено.")

        except Exception as e:
            logger.error(f"Ошибка при выполнении планового обновления: {e}")