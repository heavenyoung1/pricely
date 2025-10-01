from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher
from aiogram.types import CallbackQuery
from src.presentation.bot.utils.formatters import format_product_message
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard
from src.infrastructure.services import logger, product_service

async def choose_product_to_delete(message: types.Message):
    try:
        products = product_service.get_all_products(str(message.from_user.id))
        if not products:
            await message.answer("📭 У вас пока нет отслеживаемых товаров")
            return
        
        buttons  = []  # Список для хранения рядов кнопок
        for p in products:
            name = p.get("name") or p.get("product_name") or p.get("id")
            display = name if len(name) <= 60 else name[:57] + "..."
            buttons.append(InlineKeyboardButton(text=f"🗑 {display}", callback_data=f"delete_product:{p['id']}"))
            
            kb = InlineKeyboardMarkup(inline_keyboard=buttons)
            await message.answer("Выберите товар для удаления:", reply_markup=kb)

    except Exception as e:
        logger.exception("Ошибка при показе списка для удаления")
        await message.answer(f"❌ Ошибка: {e}")

async def handle_delete_product_request(call: CallbackQuery):
    await call.answer()  # Отправляем ответ на callback-запрос
    product_id = call.data.split(":", 1)[1]

    try:
        product = product_service.get_full_product(product_id)
        if not product:
            await call.answer("❌ Товар не найден")
            return

        keyboard = [
            InlineKeyboardButton("✅ Да, удалить", callback_data=f"confirm_delete:{product_id}"),
            InlineKeyboardButton("❌ Отмена", callback_data=f"cancel_delete:{product_id}")
        ]
        kb = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await call.message.edit_text(
            f"⚠️ Удалить товар <b>{product['name']}</b>?",
            parse_mode="HTML",
            reply_markup=kb
        )
    except Exception as e:
        logger.exception("Ошибка при запросе подтверждения удаления")
        await call.answer(f"❌ Ошибка: {e}")

# 3️⃣ Подтверждение удаления
async def handle_confirm_delete(call: CallbackQuery):
    await call.answer()  # Отправляем ответ на callback-запрос
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
            buttons.append(InlineKeyboardButton(text=display, callback_data=f"product:{p['id']}"))

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

        await call.message.edit_text(
            "🗑️ Товар удалён.\n📋 Ваши товары:",
            reply_markup=kb
        )
    except Exception as e:
        logger.exception("Ошибка при подтверждении удаления")
        await call.answer(f"❌ Ошибка: {e}")

# 4️⃣ Отмена удаления
async def handle_cancel_delete(call: CallbackQuery):
    await call.answer()  # Отправляем ответ на callback-запрос
    product_id = call.data.split(":", 1)[1]

    try:
        product = product_service.get_full_product(product_id)
        if not product:
            await call.message.edit_text("❌ Товар не найден")
            return

        text = format_product_message(product)
        kb = build_product_actions_keyboard(product_id=product["id"], product_link=product["link"])

        await call.message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=kb,
            disable_web_page_preview=False
        )
    except Exception as e:
        logger.exception("Ошибка при отмене удаления")
        await call.answer(f"❌ Ошибка: {e}")