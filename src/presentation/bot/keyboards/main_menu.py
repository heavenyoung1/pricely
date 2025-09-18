from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        KeyboardButton("➕ Добавить товар"),
        KeyboardButton("➖ Удалить товар")
    )
    kb.row(
        KeyboardButton("📋 Мои товары"),
        KeyboardButton("🗑️ Очистить отслеживаемые")
    )
    kb.row(
        KeyboardButton("⚙️ Настройки")
    )
    return kb
