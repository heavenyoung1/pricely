import os
import logging
from telebot import TeleBot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.domain.entities import Product, Price

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

def format_categories(categories) -> str:
    """Форматирует категории для красивого отображения"""
    if not categories:
        return "—"
    
    # Если это строка в формате {cat1,cat2,"cat3"}
    if isinstance(categories, str):
        if categories.startswith('{') and categories.endswith('}'):
            # Убираем фигурные скобки и разделяем по запятым
            categories_list = [cat.strip().strip('"') for cat in categories.strip('{}').split(',')]
            return ' → '.join(categories_list)
        else:
            return categories
    
    # Если это список или кортеж
    elif isinstance(categories, (list, tuple)):
        return " → ".join(str(cat) for cat in categories)
    
    # В остальных случаях просто возвращаем как строку
    return str(categories)

def format_product_message(product: dict) -> str:
    """
    Форматирует сообщение о товаре для Telegram (ожидает dict).
    """
    latest = product.get("latest_price") or {}
    text = (
        f"📦 {product.get('name')}\n"
        f"💳 Цена с картой: {latest.get('with_card', '—')}\n"
        f"💵 Цена без карты: {latest.get('without_card', '—')}\n"
        f"🔗 {product.get('link')}"
    )
    return text
