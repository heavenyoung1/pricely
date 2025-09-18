from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def confirm_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("✅ Да"), KeyboardButton("❌ Нет"))
    return kb
