# import logging
# import os
# from typing import Optional
# from requests import head
# import telebot
# from dotenv import load_dotenv
# from src.infrastructure.core.ozon_parser import OzonParser
# from src.infrastructure.services import ProductService
# from src.domain.entities import Product, Price, User
# from src.infrastructure.database.core import UnitOfWork, get_db_session

# # Настройка логирования
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('bot.log', encoding='utf-8'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# # Загрузка конфигурации из .env
# load_dotenv()
# BOT_TOKEN = os.getenv('BOT_TOKEN')
# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN не найден в .env файле")

# # Инициализация бота и сервисов
# bot = telebot.TeleBot(BOT_TOKEN)
# parser = OzonParser()
# product_service = ProductService(uow_factory=get_db_session)

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     url = message.text.strip()
#     user_id = str(message.from_user.id)

#     # Проверка, что URL с Ozon
#     if not url.startswith("https://www.ozon.ru/"):
#         bot.reply_to(message, "Ошибка: Пожалуйста, отправьте ссылку на товар с Ozon.")
#         logger.warning(f"Невалидный URL: {url} от пользователя {user_id}")
#         return
    
#     # Проверка корректности URL (HTTP-код 200)
#     try:
#         response = head(url, timeout=5, allow_redirects=True)
#         if response.status_code != 200:
#             bot.reply_to(message, f"Ошибка: URL {url} недоступен (код: {response.status_code}).")
#             logger.error(f"Недоступный URL: {url}, код: {response.status_code}")
#             return
#         logger.info(f"URL {url} доступен, начинаем парсинг")
#     except Exception as e:
#         bot.reply_to(message, f"Ошибка при проверке URL: {str(e)}")
#         logger.error(f"Ошибка проверки URL {url}: {str(e)}")
#         return
    
#     # Парсинг данных
#     try:
#         product_data = parser.parse_product(url)
#         logger.info(f"Успешно спарсены данные для {url}: {product_data}")
#     except Exception as e:
#         bot.reply_to(message, f"Ошибка при парсинге: {str(e)}")
#         logger.error(f"Ошибка парсинга {url}: {str(e)}")
#         return

#     # Создание доменных сущностей
#     try:
#         product = Product(
#             id=product_data['id'],
#             name=product_data['name'],
#             user_id=user_id,
#             categories=product_data['categories']
#         )
#         price = Price(
#             product_id=product_data['id'],
#             price_with_card=product_data['price_with_card'],
#             price_without_card=product_data['price_without_card'],
#             price_default=product_data['price_default'],
#             rating=product_data['rating'],
#             image_url=product_data['image_url']
#         )
#         user = User(id=user_id, username=message.from_user.username or "unknown")
#     except Exception as e:
#         bot.reply_to(message, f"Ошибка создания сущностей: {str(e)}")
#         logger.error(f"Ошибка создания сущностей для {url}: {str(e)}")
#         return

#     # Сохранение через ProductService
#     try:
#         product_service.create_user(user)
#         product_service.create_product(user_id, product, price)
#         logger.info(f"Данные для {url} сохранены в БД для пользователя {user_id}")
#     except Exception as e:
#         bot.reply_to(message, f"Данные отправлены, но ошибка сохранения в БД: {str(e)}")
#         logger.error(f"Ошибка сохранения в БД для {url}: {str(e)}")
#         return

#     # Формирование ответа
#     response_text = (
#         f"Название товара: {product_data['name']}\n"
#         f"ID товара: {product_data['id']}\n"
#         f"Рейтинг товара: {product_data['rating']}\n"
#         f"Цена с картой: {product_data['price_with_card']}\n"
#         f"Цена без карты: {product_data['price_without_card']}\n"
#         f"Базовая цена: {product_data['price_default']}\n"
#         f"URL изображения: {product_data['image_url']}\n"
#         f"Категории: {', '.join(product_data['categories'])}"
#     )
#     bot.reply_to(message, response_text)

# if __name__ == "__main__":
#     logger.info("Запуск Telegram-бота")
#     try:
#         bot.polling()
#     except Exception as e:
#         logger.error(f"Ошибка работы бота: {str(e)}")
#         raise



import os
import logging
from telebot import TeleBot
from dotenv import load_dotenv
import logging
from handlers import start, marketplace, products, settings

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
marketplace.register_handlers(bot)
products.register_handlers(bot)
settings.register_handlers(bot)

if __name__ == "__main__":
    logger.info("Запуск Telegram-бота")
    bot.infinity_polling()
