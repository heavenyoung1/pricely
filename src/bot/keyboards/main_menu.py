from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        KeyboardButton("📦 Выбрать маркетплейс"),
        KeyboardButton("➕ Добавить товар")
    )
    kb.row(
        KeyboardButton("➖ Удалить товар"),
        KeyboardButton("📋 Мои товары")
    )
    kb.row(
        KeyboardButton("⚙️ Настройки")
    )
    return kb

def marketplaces():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    kb.add(KeyboardButton("🟦 Ozon"), KeyboardButton("🟪 Wildberries"))
    kb.add(KeyboardButton("⬅️ Назад"))
    return kb
