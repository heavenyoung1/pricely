import logging
import threading
from src.presentation.bot.bot_instance import bot
from src.presentation.bot.handlers import start, products, menu, delete, navigation, statistics, errors
from src.infrastructure.parsers import OzonParser
from src.infrastructure.notifications.notification_service import NotificationService
from src.infrastructure.scheduler import start_scheduler

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Регистрация всех хендлеров
def register_handlers():
    start.register_handlers(bot)
    statistics.register_handlers(bot)
    errors.register_handlers(bot)
    navigation.register_handlers(bot)
    products.register_handlers(bot)
    menu.register_handlers(bot)
    delete.register_handlers(bot)

def main():
    logger.info("Запуск Telegram-бота...")

    # Проверка и отключение вебхука (на всякий случай, если раньше использовался)
    try:
        webhook_info = bot.get_webhook_info()
        logger.info(f"Webhook info before polling: {webhook_info.to_dict()}")
        if webhook_info.url:
            bot.remove_webhook()
            logger.info("Удалён старый webhook")
    except Exception as e:
        logger.warning(f"Ошибка при проверке webhook: {e}")

        # Запускаем планировщик цен в фоновом режиме
        start_scheduler()

        # Запускаем polling
        bot.infinity_polling(none_stop=True, interval=0, timeout=20, logger_level=logging.DEBUG)

if __name__ == "__main__":
    main()