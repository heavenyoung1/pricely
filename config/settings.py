from dotenv import load_dotenv
import os

from utils.logger import logger

# Загружаем переменные из .env
load_dotenv()

# Telegram
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

if not bot_token or not chat_id:
    logger.error('Отсутствуют BOT_TOKEN или CHAT_ID в .env файле')
    raise ValueError("Отсутствуют BOT_TOKEN или CHAT_ID в .env файле")