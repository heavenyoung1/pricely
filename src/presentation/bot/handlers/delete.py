import logging
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from src.infrastructure.services import product_service
from src.presentation.bot.utils.formatters import format_product_message
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard

logger = logging.getLogger(__name__)


async def choose_product_to_delete(message: Message, product_service):
    """Показываем список товаров для удаления"""
    try:
        products = product_service.get_all_products(str(message.from_user.id))
        if not products:
            await message.answer("📭 У вас пока нет отслеживаемых товаров")
            return

        buttons = []
        for p in products:
            name = p.get("name") or p.get("product_name") or p.get("id")
            display = name if len(name) <= 60 else name[:57] + "..."
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"🗑 {display}", callback_data=f'delete_product:{p["id"]}'
                    )
                ]
            )

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("📋 Выберите товар для удаления:", reply_markup=kb)

    except Exception as e:
        logger.exception("Ошибка при показе списка для удаления")
        await message.answer("❌ Произошла ошибка. Попробуйте ещё раз.")


async def handle_delete_product_request(call: CallbackQuery, product_service):
    """Запрос подтверждения удаления"""
    await call.answer()
    product_id = call.data.split(":", 1)[1]

    try:
        product = product_service.get_full_product(product_id)
        if not product:
            await call.message.edit_text("❌ Товар не найден")
            return

        # ✅ Правильный синтаксис aiogram 3.x
        keyboard = [
            [
                InlineKeyboardButton(
                    text="✅ Да, удалить", callback_data=f"confirm_delete:{product_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отмена", callback_data=f"cancel_delete:{product_id}"
                ),
            ]
        ]
        kb = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await call.message.edit_text(
            f'⚠️ Удалить товар <b>{product["name"]}</b>?',
            parse_mode="HTML",
            reply_markup=kb,
        )
    except Exception as e:
        logger.exception("Ошибка при запросе подтверждения удаления")
        try:
            await call.message.edit_text("❌ Произошла ошибка. Попробуйте ещё раз.")
        except Exception:
            await call.message.answer("❌ Произошла ошибка. Попробуйте ещё раз.")


async def handle_confirm_delete(call: CallbackQuery, product_service):
    """Подтверждение удаления"""
    await call.answer()
    product_id = call.data.split(":", 1)[1]

    try:
        product_service.delete_product(product_id)

        products = product_service.get_all_products(str(call.from_user.id))
        if not products:
            await call.message.edit_text(
                "🗑️ Товар удалён.\n📭 У вас больше нет отслеживаемых товаров."
            )
            return

        buttons = []
        for p in products:
            name = p.get("name") or p.get("product_name") or p.get("id")
            display = name if len(name) <= 60 else name[:57] + "..."
            buttons.append(
                [InlineKeyboardButton(text=display, callback_data=f'product:{p["id"]}')]
            )

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

        await call.message.edit_text(
            "🗑️ Товар удалён.\n📋 Ваши товары:", reply_markup=kb
        )
    except Exception as e:
        logger.exception("Ошибка при подтверждении удаления")
        try:
            await call.message.edit_text(
                "❌ Произошла ошибка при удалении. Попробуйте ещё раз."
            )
        except Exception:
            await call.message.answer(
                "❌ Произошла ошибка при удалении. Попробуйте ещё раз."
            )


async def handle_cancel_delete(call: CallbackQuery, product_service):
    """Отмена удаления"""
    await call.answer()
    product_id = call.data.split(":", 1)[1]

    try:
        product = product_service.get_full_product(product_id)
        if not product:
            await call.message.edit_text("❌ Товар не найден")
            return

        text = format_product_message(product)
        kb = build_product_actions_keyboard(
            product_id=product["id"], product_link=product["link"]
        )

        await call.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=kb,
            disable_web_page_preview=False,
        )
    except Exception as e:
        logger.exception("Ошибка при отмене удаления")
        try:
            await call.message.edit_text("❌ Произошла ошибка. Попробуйте ещё раз.")
        except Exception:
            await call.message.answer("❌ Произошла ошибка. Попробуйте ещё раз.")
