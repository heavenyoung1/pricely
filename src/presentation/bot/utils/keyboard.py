from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_product_actions_keyboard(
    product_id: str, product_link: str
) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с действиями над товаром.
    В aiogram 3.x клавиатура создается через список списков кнопок.
    """
    keyboard = [
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_products"),
            InlineKeyboardButton(
                text="🗑 Удалить", callback_data=f"delete_product:{product_id}"
            ),
        ],
        [
            InlineKeyboardButton(text="Открыть на Ozon", url=product_link),
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
