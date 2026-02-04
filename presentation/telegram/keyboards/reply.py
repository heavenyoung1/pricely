from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Константы для текста кнопок (используются в фильтрах)
BTN_ADD_PRODUCT = '➕ Добавить товар'
BTN_MY_PRODUCTS = '📋 Мои товары'
REMOVE_MY_PRODUCT = '➖ Удалить товар'
INFO = '📖 Справка'


def main_menu() -> ReplyKeyboardMarkup:
    '''Главное меню (постоянная клавиатура)'''
    buttons = [
        [
            KeyboardButton(text=BTN_ADD_PRODUCT),
            KeyboardButton(text=BTN_MY_PRODUCTS),
            KeyboardButton(text=REMOVE_MY_PRODUCT),
            KeyboardButton(text=INFO),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
