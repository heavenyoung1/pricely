import logging
from apscheduler.schedulers.background import BackgroundScheduler
from src.presentation.bot.service_connector import service

logger = logging.getLogger(__name__)


def check_prices_for_all_users():
    """Проходит по всем пользователям и обновляет цены на их товары"""
    logger.info("🔄 Запуск проверки цен...")

    try:
        # Получаем всех пользователей
        uow = service.uow_factory()
        users = uow.user_repository.get_all()

        for user in users:
            products = service.get_all_products(str(user.id))
            for product in products:
                service.update_product_price(product["id"])

        logger.info("✅ Проверка цен завершена")

    except Exception as e:
        logger.error(f"Ошибка при проверке цен: {e}")


def start_scheduler():
    """Запускает APScheduler в фоне"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_prices_for_all_users, "interval", minutes=30)  # каждые 30 минут
    scheduler.start()

    logger.info("✅ Планировщик запущен (проверка каждые 30 минут)")
    return scheduler
