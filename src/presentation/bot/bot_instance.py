import os
from telebot import TeleBot
from dotenv import load_dotenv
import logging
from src.domain.exceptions import ProductNotFoundError
from .service_connector import service
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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

def build_products_keyboard(products: list) -> InlineKeyboardMarkup:
    keyboard = []
    for product in products:
        keyboard.append([InlineKeyboardButton(
            text=product.name,
            callback_data=f"product:{product.id}"
        )])
    # Добавляем кнопку "Назад"
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# РАБОЧИЙ ВАРИАНТ
# def build_product_actions_keyboard(product_id: str, product_link: str) -> InlineKeyboardMarkup:
#     kb = InlineKeyboardMarkup(row_width=2)
#     kb.add(
#         InlineKeyboardButton("Обновить цену", callback_data=f"update_price:{product_id}"),
#         InlineKeyboardButton("Удалить товар", callback_data=f"delete_product:{product_id}")
#     )
#     kb.add(InlineKeyboardButton("Открыть на Ozon", url=product_link))
#     return kb

# НЕРАБОЧИЙ ВАРИАНТ!
def build_product_actions_keyboard(product_id: str, product_link: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Обновить цену", callback_data=f"update_price:{product_id}"),
        InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_product:{product_id}")
    )
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_products"))
    kb.add(InlineKeyboardButton("Открыть на Ozon", url=product_link))
    return kb


    #kb.add(InlineKeyboardButton("Открыть на Ozon", url=product_link))

def format_product_message(product: dict) -> str:
    latest = product.get("latest_price") or {}
    with_card = latest.get("with_card")
    without_card = latest.get("without_card")
    default = latest.get("default")

    with_card_text = f"{with_card} ₽" if with_card is not None else "—"
    without_card_text = f"{without_card} ₽" if without_card is not None else "—"
    default_text = f"{default} ₽" if default is not None else "—"

    categories = product.get("categories")
    # categories может быть либо строкой, либо списком
    if isinstance(categories, (list, tuple)):
        categories_text = " > ".join(categories)
    else:
        categories_text = str(categories or "—")

    text = (
        f"🏷️ <b>{product.get('name','(без названия)')}</b>\n"
        f"🔢 ID: <code>{product.get('id')}</code>\n"
        f"💳 Цена (с картой): {with_card_text}\n"
        f"💸 Цена (без карты): {without_card_text}\n"
        f"💠 Базовая цена: {default_text}\n"
        f"⭐ Рейтинг: {product.get('rating', '—')}\n"
        f"🗂 Категории: {categories_text}\n\n"
        f"🔗 <a href=\"{product.get('link')}\">Открыть на Ozon</a>"
    )
    return text

@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("product:"))
def handle_product_button(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    product_id = call.data.split(":", 1)[1]

    try:
        product = service.get_full_product(product_id)  # должен вернуть dict
        if not product:
            bot.send_message(call.message.chat.id, "❌ Товар не найден.")
            return

        text = format_product_message(product)  # у тебя в bot_instance уже есть
        kb = build_product_actions_keyboard(product_id=product["id"], product_link=product["link"])

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=kb,
            disable_web_page_preview=False
        )
    except ProductNotFoundError:
        bot.answer_callback_query(call.id, "❌ Товар удалён или не найден")
    except Exception as e:
        logger.exception("Ошибка в handle_product_button")
        bot.answer_callback_query(call.id, f"Ошибка: {e}")