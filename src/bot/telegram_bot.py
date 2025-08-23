import logging
import os
from typing import Optional
from requests import head
import telebot
from dotenv import load_dotenv
from src.infrastructure.core.ozon_parser import OzonParser
from src.infrastructure import ProductService
from src.domain.entities import Product, Price, User
from src.infrastructure.database.core import UnitOfWork, get_db_session

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Загрузка конфигурации из .env
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

# Инициализация бота и сервисов
bot = telebot.TeleBot(BOT_TOKEN)
parser = OzonParser()
product_service = ProductService(uow_factory=get_db_session)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    user_id = str(message.from_user.id)

    # Проверка, что URL с Ozon
    if not url.startswith("https://www.ozon.ru/"):
        bot.reply_to(message, "Ошибка: Пожалуйста, отправьте ссылку на товар с Ozon.")
        logger.warning(f"Невалидный URL: {url} от пользователя {user_id}")
        return
    
    # Проверка корректности URL (HTTP-код 200)
    try:
        response = head(url, timeout=5, allow_redirects=True)
        if response.status_code != 200:
            bot.reply_to(message, f"Ошибка: URL {url} недоступен (код: {response.status_code}).")
            logger.error(f"Недоступный URL: {url}, код: {response.status_code}")
            return
        logger.info(f"URL {url} доступен, начинаем парсинг")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при проверке URL: {str(e)}")
        logger.error(f"Ошибка проверки URL {url}: {str(e)}")
        return
    
    # Парсинг данных
    try:
        product_data = parser.parse_product(url)
        logger.info(f"Успешно спарсены данные для {url}: {product_data}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при парсинге: {str(e)}")
        logger.error(f"Ошибка парсинга {url}: {str(e)}")
        return