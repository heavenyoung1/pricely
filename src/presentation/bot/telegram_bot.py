import logging
from src.presentation.bot.bot_instance import bot
from src.presentation.bot.handlers import start # Импортируем start.py для регистрации обработчиков
from telebot.handler_backends import StatesGroup, State
from telebot.storage import StateMemoryStorage

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Проверяем текущий вебхук
        webhook_info = bot.get_webhook_info()
        logger.info(f"Webhook info before polling: {webhook_info}")
        
        # Удаляем вебхук, если он существует
        if webhook_info.url:
            logger.warning(f"Found active webhook: {webhook_info.url}. Deleting...")
            bot.delete_webhook()
            logger.info("Webhook successfully deleted")
        else:
            logger.info("No active webhook found")
        
        # Проверяем получение обновлений
        logger.info("Checking for updates manually")
        updates = bot.get_updates(timeout=5)
        logger.debug(f"Received updates: {updates}")
        
        # Запускаем polling
        logger.info("Starting bot polling")
        bot.infinity_polling(none_stop=True, interval=0, timeout=20, logger_level=logging.DEBUG)
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
        raise