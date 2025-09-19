import os
from telebot import TeleBot
from dotenv import load_dotenv
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
logger.info(f"Loaded BOT_TOKEN: {BOT_TOKEN[:10]}...")  # Показываем только начало
if not BOT_TOKEN:
    logger.error('BOT_TOKEN not found in .env')
    raise ValueError('BOT_TOKEN не найден в .env')

bot = TeleBot(BOT_TOKEN, parse_mode='HTML')
logger.info("Bot initialized successfully")