import os
import logging
from telebot import TeleBot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Загружаем токен
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

bot = TeleBot(BOT_TOKEN, parse_mode="HTML")

# ==== УТИЛИТЫ ====

def build_product_actions_keyboard(product_id: str, product_link: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Обновить цену", callback_data=f"update_price:{product_id}"),
        InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_product:{product_id}")
    )
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_products"))
    kb.add(InlineKeyboardButton("Открыть на Ozon", url=product_link))
    return kb

def format_product_message(product: dict) -> str:
    latest = product.get("latest_price") or {}
    with_card = latest.get("with_card")
    without_card = latest.get("without_card")

    with_card_text = f"{with_card} ₽" if with_card is not None else "—"
    without_card_text = f"{without_card} ₽" if without_card is not None else "—"

    categories = product.get("categories")
    if isinstance(categories, (list, tuple)):
        categories_text = " > ".join(categories)
    else:
        categories_text = str(categories or "—")

    return (
        f"🏷️ <b>{product.get('name','(без названия)')}</b>\n"
        f"🔢 ID: <code>{product.get('id')}</code>\n"
        f"💳 Цена (с картой): {with_card_text}\n"
        f"💸 Цена (без карты): {without_card_text}\n"
        f"⭐ Рейтинг: {product.get('rating', '—')}\n"
        f"🗂 Категории: {categories_text}\n\n"
        f"🔗 <a href=\"{product.get('link')}\">Открыть на Ozon</a>"
    )
