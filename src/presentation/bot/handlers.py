import telebot
from telebot.types import Message
from src.infrastructure.services import ProductService
from src.domain.entities import User, Price
from src.core import SQLAlchemyUnitOfWork

from presentation.bot import main_menu

# Создание бота
bot = telebot.TeleBot("YOUR_TOKEN")

# Сервисный слой
service = ProductService(uow_factory=SQLAlchemyUnitOfWork)

# ====================== СТАРТ ======================
@bot.message_handler(commands=["start"])
def start(message: Message):
    user = User(
        id=str(message.from_user.id),
        username=message.from_user.username or "unknown",
        chat_id=str(message.chat.id),
        products=[]
    )
    try:
        service.create_user(user)
    except Exception:
        pass  # юзер уже есть
    bot.send_message(message.chat.id, "Добро пожаловать! 👋", reply_markup=main_menu())

# ====================== ДОБАВИТЬ ТОВАР ======================
@bot.message_handler(func=lambda m: m.text == "➕ Добавить товар")
def add_product_request(message: Message):
    bot.send_message(message.chat.id, "📦 Отправь ссылку на товар с Ozon")
    bot.register_next_step_handler(message, add_product_process)

def add_product_process(message: Message):
    url = message.text.strip()
    try:
        result = service.create_product(str(message.from_user.id), url)
        bot.send_message(
            message.chat.id,
            f"✅ Товар добавлен!\n\n"
            f"Название: {result['name']}\n"
            f"Цена с картой: {result['with_card']} ₽\n"
            f"Цена без карты: {result['without_card']} ₽"
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

# ====================== МОИ ТОВАРЫ ======================
@bot.message_handler(func=lambda m: m.text == "📋 Мои товары")
def list_products(message: Message):
    try:
        products = service.get_full_product_list(str(message.from_user.id))  # ⚡ нужно реализовать в сервисе
        if not products:
            bot.send_message(message.chat.id, "📭 У вас пока нет отслеживаемых товаров")
            return
        text = "📋 Ваши товары:\n\n"
        for p in products:
            latest = p["latest_price"]
            text += f"{p['name']} — {latest['with_card']} ₽ (с картой)\n"
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

# ====================== УДАЛИТЬ ТОВАР ======================
@bot.message_handler(func=lambda m: m.text == "➖ Удалить товар")
def delete_product_request(message: Message):
    bot.send_message(message.chat.id, "❌ Введи артикул товара, который хочешь удалить")
    bot.register_next_step_handler(message, delete_product_process)

def delete_product_process(message: Message):
    product_id = message.text.strip()
    try:
        service.delete_product(product_id)
        bot.send_message(message.chat.id, f"✅ Товар {product_id} удалён")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

# ====================== ОЧИСТИТЬ ВСЕ ======================
@bot.message_handler(func=lambda m: m.text == "🗑️ Очистить отслеживаемые")
def clear_products(message: Message):
    try:
        # Нужно сделать usecase в сервисе: delete_all_products(user_id)
        service.delete_all_products(str(message.from_user.id))
        bot.send_message(message.chat.id, "🗑️ Все товары удалены")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

# ====================== RUN ======================
# if __name__ == "__main__":
#     print("🚀 Бот запущен")
#     bot.infinity_polling()
