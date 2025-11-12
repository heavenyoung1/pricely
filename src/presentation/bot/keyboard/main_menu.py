from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu() -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру с кнопками для добавления товара, статистики и других опций.
    :return: клавиатура
    """
    buttons = [
        [
            KeyboardButton(text="➕ Добавить товар"),
            KeyboardButton(text="📋 Мои товары"),
        ],
        [
            KeyboardButton(text="➖ Удалить товар"),
            KeyboardButton(text="📖 Справка"),
        ],
    ]

    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return kb
