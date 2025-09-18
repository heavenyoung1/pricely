from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(
        KeyboardButton("➕ Добавить товар"),
        KeyboardButton("📋 Мои товары")
    )
    kb.row(
        KeyboardButton("➖ Удалить товар"),
        KeyboardButton("🗑️ Очистить все")
    )
    kb.row(
        KeyboardButton("📊 Статистика"),
        KeyboardButton("ℹ️ Помощь")
    )
    return kb
