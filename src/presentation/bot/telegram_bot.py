import os
import logging
from telebot import TeleBot
from dotenv import load_dotenv
import logging
from .handlers import (
    start,
    add_product_request,
    list_products,
    delete_product_request,
    clear_products,
)
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ozon_parser.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Загружаем конфиг
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

# Инициализация
bot = TeleBot(BOT_TOKEN, parse_mode="HTML")

# Подключаем хендлеры
start.register_handlers(bot)
add_product_request.register_handlers(bot)
list_products.register_handlers(bot)
delete_product_request.register_handlers(bot)
clear_products.register_handlers(bot)

if __name__ == "__main__":
    logger.info("Запуск Telegram-бота")
    bot.infinity_polling()
