from src.infrastructure.services import logger, product_service
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard
from src.presentation.bot.handlers.products import _build_price_update_message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime


class APSchedulerService:
    def __init__(self, bot, interval_minutes=10):
        '''
        Инициализация APScheduler для планирования задач.

        :param parser: Парсер для выполнения задачи
        :param interval_minutes: Интервал в минутах для запуска задачи (по умолчанию 10 минут)
        '''
        self.scheduler = BackgroundScheduler()
        self.bot = bot
        self.interval_minutes = interval_minutes

        self.scheduler.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    def start(self):
        self.scheduler.add_job(self.run_price_update, 'interval', minutes=self.interval_minutes, id="parse_product")
        self.scheduler.start()
        logger.info(f"APScheduler запущен (каждые {self.interval_minutes} минут).")

    def stop(self):
        self.scheduler.shutdown()
        logger.info("APScheduler остановлен.")

    async def run_price_update(self):
        logger.info("🚀 Автоматический парсинг начался...")

        try:
            products = product_service.get_all_products_for_update()
            if not products:
                logger.info("Нет товаров для обновления.")
                return

            for product in products:
                try:
                    await product_service.update_product_price(product["id"])
                except Exception as e:
                    logger.error(f"Ошибка обновления товара {product['id']}: {e}")

        except Exception as e:
            logger.error(f"Ошибка при выполнении планового обновления: {e}")

        logger.info("✅ Автоматический парсинг завершён.")