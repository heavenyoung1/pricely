from aiogram.types import Message

async def fallback(message: Message):
    await message.answer("❓ Неизвестная команда. Напишите /help")