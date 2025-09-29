from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def build_product_actions_keyboard(product_id: str, product_link: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔄 Обновить цену", callback_data=f"update_price:{product_id}"),
        InlineKeyboardButton("🗑 Удалить", callback_data=f"delete_product:{product_id}")
    )
    kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_products"))
    kb.add(InlineKeyboardButton("Открыть на Ozon", url=product_link))
    return kb