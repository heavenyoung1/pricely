from telebot.types import Message
from requests import head
import logging
import sys
import uuid

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

        # Парсинг данных
        try:
            bot.send_message(message.chat.id, f'Процесс записи данных начат, ожидайте.')
            product_data = parser.parse_product(url)
            logger.info(f'Успешно спарсены данные для {url}: {product_data}')
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка при парсинге: {str(e)}. Проверь ссылку.", reply_markup=main_menu())
            logger.error(f"Ошибка парсинга URL {url} для пользователя {user_id}: {str(e)}")
            return
        
        # Создание доменных сущностей
        try:
            product = Product (
                id = product_data['id'],
                user_id=user_id,
                price_id=str(uuid.uuid4()),
                name=product_data['name'],
                link=url,
                image_url=product_data['image_url'],
                rating=product_data['rating'],
                categories=product_data['categories']
            )

            price = Price(
                id 
            )
            
        except Exception as e:
            raise