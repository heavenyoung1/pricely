from telebot.types import Message
from requests import head
import logging
import sys
import uuid
from datetime import datetime

from src.bot.keyboards.main_menu import main_menu
from src.infrastructure.core.ozon_parser import OzonParser
from src.infrastructure.services import ProductService
from src.domain.entities import Product, Price, User
from src.infrastructure.database.core import get_db_session


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ozon_parser.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# состояния пользователей
user_states = {}

# сервисы
parser = OzonParser()
product_service = ProductService(uow_factory=get_db_session)

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "➕ Добавить товар")
    def add_product(message: Message):
        user_states[message.chat.id] = "waiting_for_product_url"
        bot.send_message(message.chat.id, "Отправь ссылку на товар (например с Ozon).")

    @bot.message_handler(func=lambda m: m.text == "➖ Удалить товар")
    def remove_product(message: Message):
        bot.send_message(message.chat.id, "Выбери товар для удаления (пока заглушка).")

    @bot.message_handler(func=lambda m: m.text == "📋 Мои товары")
    def list_products(message: Message):
        bot.send_message(message.chat.id, "Твои отслеживаемые товары (пока заглушка).")

    # обработка ссылки на товар
    @bot.message_handler(func=lambda m: user_states.get(m.chat.id) == 'waiting_for_product_url')
    def handle_product_url(message: Message):
        url = message.text.strip()
        user_id = str(message.from_user.id)

        # Запуск процесса через сервис
        result = product_service.create_product(user_id, url)

        # Обработка результата
        if result["success"]:
            bot.send_message(message.chat.id, result["message"], reply_markup=main_menu())
        else:
            bot.send_message(message.chat.id, result["message"], reply_markup=main_menu())
        logger.info(f"Обработка URL {url} для пользователя {user_id} завершена: {result['message']}")

        # Сброс состояния
        del user_states[message.chat.id]